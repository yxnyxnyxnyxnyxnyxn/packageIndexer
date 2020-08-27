import queue
import select
import socket
from package_indexer import PackageIndexer
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

PORT = 8080
ERROR = 'ERROR\n'

indexer = PackageIndexer()

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(('0.0.0.0', PORT))
    server.listen(10)

    inputs = [server]
    outputs = []
    message_queues = {}
    cnt = 1
    logging.info('starting server')
    while inputs:
        cnt += 1
        ready_to_read, ready_to_write, exceptional = select.select(inputs, outputs, [])

        for s in ready_to_read:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)

                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    msg = data.decode('utf-8').strip()
                    logging.info(msg)
                    command, package, dependencies = indexer.validate_msg(msg)

                    result = ERROR
                    if command != "ERROR":
                        if command == "INDEX":
                            result = indexer.index(package, dependencies)
                        elif command == "REMOVE":
                            result = indexer.remove(package)
                        elif command == "QUERY":
                            result = indexer.query(package)
                    message_queues[s].put(result)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)

                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in ready_to_write:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            except KeyError:
                pass
            else:
                s.send(next_msg.encode('utf-8'))

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            del message_queues[s]

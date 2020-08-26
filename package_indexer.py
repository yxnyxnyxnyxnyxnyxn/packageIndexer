OK = 'OK\n'
FAIL = 'FAIL\n'
ERROR = 'ERROR\n'


class PackageIndexer:
    def __init__(self):
        self.INDEX = {}
        self.PackageMap = {}

    def remove(self, package):
        if package not in self.INDEX:
            return OK
        if package in self.PackageMap:
            return FAIL

        keys = [k for k in self.PackageMap]
        for k in keys:
            dependants = self.PackageMap[k]
            if package in dependants:  # if package if one of dependant of the package , remove it from set
                dependants.remove(package)

            if len(dependants) == 0:  # if nothing is depended on the package, remove it from the packageMap
                del self.PackageMap[k]
        del self.INDEX[package]
        return OK

    def index(self, package, dependencies):

        if dependencies is not None:
            for d in dependencies:
                if d not in self.INDEX:
                    return FAIL
                if d not in self.PackageMap:  # if dependency not in PackageMap add it
                    self.PackageMap[d] = {package}  # set PackageMap[dependency]
                else:  # if dependency already there add to the set
                    self.PackageMap[d].add(package)

        self.INDEX[package] = dependencies
        return OK

    def query(self, package):
        if package in self.INDEX:
            return OK
        else:
            return FAIL

    def validate_msg(self, msg):

        parsed_msg = msg.split('|')

        if len(parsed_msg) != 3:
            return ERROR, 'Missing mandatory arguments', None

        if not parsed_msg[1] or ',' in parsed_msg[1]:
            return ERROR, 'Invalid package name', None

        if parsed_msg[0] not in ['INDEX', 'REMOVE', 'QUERY']:
            return ERROR, 'Invalid command', None

        dependencies = parsed_msg[2].split(',')
        if dependencies == ['']:
            dependencies = None
        return parsed_msg[0], parsed_msg[1], dependencies

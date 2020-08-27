FROM python:3
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/yxnyxnyxnyxnyxnyxn/packageIndexer.git /usr/src/app/
RUN python /usr/src/app/tests.py
EXPOSE 8080
CMD ["python", "-u", "/usr/src/app/server.py"]
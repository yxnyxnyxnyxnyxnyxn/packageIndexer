FROM python:3.7
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/yxnyxnyxnyxnyxnyxn/packageIndexer.git /usr/src/app/
RUN python3 /usr/src/app/tests.py
EXPOSE 8080
CMD ["python3", "-u", "/usr/src/app/server.py","--host=0.0.0.0"]
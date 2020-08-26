# FROM python:3.7
# RUN apt-get update && apt-get install -y git
# RUN git clone https://github.com/yxnyxnyxnyxnyxnyxn/packageIndexer.git /usr/src/app/
# RUN python /usr/src/app/unit_tests.py
# EXPOSE 8080
# CMD ["python3", "-u", "/usr/src/app/server.py"]
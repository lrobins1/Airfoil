FROM quay.io/fenicsproject/stable:current
USER root
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install celery
RUN pip install python-novaclient
ENTRYPOINT celery -A app.celery worker --loglevel=info -n worker1@%h

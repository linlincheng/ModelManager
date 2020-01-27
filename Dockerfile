FROM python:3

RUN mkdir -p /opt/albergo

COPY requirement.txt /opt/albergo/requirement.txt
RUN pip install -r /opt/albergo/requirement.txt

COPY ./python /opt/albergo/python/
COPY ./test /opt/albergo/test/
COPY ./playground.ipynb /opt/albergo/playground.ipynb
WORKDIR /opt/albergo

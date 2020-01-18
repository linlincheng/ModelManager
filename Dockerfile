FROM python:3

RUN mkdir -p /opt/albergo

COPY . /opt/albergo/.

WORKDIR /opt/albergo

CMD ["python", "./python/baseFramework.py"]
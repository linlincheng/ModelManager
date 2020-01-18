#!/usr/bin/env bash

# build base image
docker build -t albergo .

docker build -t albergo_interactive -f Dockerfile-jupyter .
docker run -p 8989:8888 \
    -v "$(pwd)/.":/opt/albergo/.\
    albergo_interactive
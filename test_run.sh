#!/usr/bin/env bash

docker build -t albergo .

if [ ! "$(docker ps -q -f name=albergo)" ]; then
    if [ "$(docker ps -aq -f status=exited -f name=albergo)" ]; then
        # cleanup
        docker rm albergo
    fi
    # run your container
    docker run -d -P --name albergo -v "$(pwd)/.":/opt/albergo/ \
  -v "$(pwd)/.":/opt/albergo/ \
  -v "$(pwd)/.":/opt/albergo/ albergo
fi

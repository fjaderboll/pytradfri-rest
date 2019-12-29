#!/bin/bash -e

port=80
if [ ! -z "$1" ]; then
    port=$1
fi

CONTAINER_NAME=pytradfri-rest
IMAGE_NAME=pytradfri-rest

docker stop $CONTAINER_NAME > /dev/null 2>&1 && echo "Stopping previous container" || echo -n ""
docker rm $CONTAINER_NAME > /dev/null 2>&1 && echo "Removing previous container" || echo -n ""
docker run -d --restart unless-stopped --name $CONTAINER_NAME -p $port:80 $IMAGE_NAME
echo "Container \"$CONTAINER_NAME\" started using port $port"

#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

options=
if [ "$1" = "-c" ]; then
    options="--no-cache"
fi
arch=$(uname -m)
if [ "$arch" = "armv7l" ]; then
    options="$options --build-arg imageName=arm32v7/python:3.11"
fi

docker build ${options} -t pytradfri-rest -f Dockerfile ..

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

mkdir -p tmp
cp -r ../rest tmp/.
rm -fr `find tmp/ -type d -name __pycache__`
cp ../requirements.txt tmp/.
docker build ${options} -t pytradfri-rest .
rm -r tmp

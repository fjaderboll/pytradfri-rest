#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

options=
if [ "$1" = "-c" ]; then
    options="--no-cache"
fi

mkdir -p tmp
cp ../rest.py tmp/.
cp ../requirements.txt tmp/.
docker build ${options} -t pytradfri-rest .
rm -r tmp

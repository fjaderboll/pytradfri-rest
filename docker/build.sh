#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

options=
if [ "$1" = "-c" ]; then
    options="--no-cache"
fi

mkdir -p tmp
cp -r ../rest tmp/.
rm -r `find tmp/ -type d -name __pycache__`
cp ../requirements.txt tmp/.
docker build ${options} -t pytradfri-rest .
rm -r tmp

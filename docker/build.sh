#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

cp ../rest.py .
docker build -t pytradfri-rest .
rm rest.py

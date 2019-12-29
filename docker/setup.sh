#!/bin/bash -e

apt-get update
apt-get install -y python3-pip python3-klein autoconf libtool wget git
pip3 install --upgrade pytradfri

mkdir /tmp/install-temp
cd /tmp/install-temp
wget https://raw.githubusercontent.com/ggravlingen/pytradfri/master/script/install-coap-client.sh
chmod a+x install-coap-client.sh
./install-coap-client.sh
cd /tmp
rm -r /tmp/install-temp

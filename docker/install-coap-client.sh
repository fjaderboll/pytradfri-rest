#!/bin/bash -e

apt-get install -y wget git autoconf libtool

mkdir /tmp/install-temp
cd /tmp/install-temp
wget https://raw.githubusercontent.com/home-assistant-libs/pytradfri/master/script/install-coap-client.sh
chmod a+x install-coap-client.sh
./install-coap-client.sh
cd /tmp
rm -r /tmp/install-temp

#!/bin/bash -e

# The original script: https://raw.githubusercontent.com/home-assistant-libs/pytradfri/refs/tags/14.0.0/script/install-coap-client.sh
# is broken partly by changes in GitHub but mostly since the repo https://github.com/home-assistant/libcoap.git
# has been deleted.

# This script works around that.

cd $(dirname "${BASH_SOURCE[0]}")

install_coap_client() {
	./autogen.sh
	./configure --disable-documentation --disable-shared --without-debug CFLAGS="-D COAP_DEBUG_FD=stderr"
	make
	make install
}

temp_dir="/tmp/coap-client-install"
apt-get install -y autoconf automake libtool

mkdir -p "$temp_dir"
cp libcoap-4.1.2.zip "$temp_dir/"
cd "$temp_dir"

unzip libcoap-4.1.2.zip
cd libcoap-4.1.2
install_coap_client

cd /tmp
rm -r "$temp_dir"

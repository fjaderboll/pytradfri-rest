#!/bin/bash -e

# The original script: https://raw.githubusercontent.com/home-assistant-libs/pytradfri/refs/tags/14.0.0/script/install-coap-client.sh
# is broken due to:
# - repo deleted: https://github.com/home-assistant/libcoap.git
# - original repo's (https://github.com/obgm/libcoap.git) submodule (tinydtls) moved

# This script works around that.

cd $(dirname "${BASH_SOURCE[0]}")

install_coap_client() {
	./autogen.sh
	./configure --disable-documentation --disable-shared --without-debug CFLAGS="-D COAP_DEBUG_FD=stderr"
	make
	make install
}

apt-get install -y autoconf automake libtool # already installed in 'python:3.11-bullseye'

temp_dir="/tmp/coap-client-install"
mkdir -p "$temp_dir"
cd "$temp_dir"

git clone --depth 1 -b dtls https://github.com/obgm/libcoap.git
cd libcoap
sed -i 's|url = .*tinydtls.*|url = https://github.com/eclipse-tinydtls/tinydtls.git|g' .gitmodules
git submodule update --init --recursive

install_coap_client

cd /tmp
rm -r "$temp_dir"

# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/ggravlingen/pytradfri) project and adds a REST API for simpler usage.

## Installation
```shell
sudo apt install python3-klein
sudo pip3 install pytradfri

cd /tmp
git clone https://github.com/ggravlingen/pytradfri.git
cd pytradfri/script/
sudo ./install-coap-client.sh
```

## Running
```shell
./rest.py 2080
```
This will start the REST API at http://localhost:2080/

## Usage
...

## Setup development
```shell
sudo apt-get install build-essential autoconf automake libtool
git clone --recursive https://github.com/obgm/libcoap.git
cd libcoap
git checkout dtls
git submodule update --init --recursive
./autogen.sh
./configure --disable-documentation --disable-shared
make
sudo make install
```

```shell
sudo apt install python3-dev
sudo pip install --upgrade pytradfri cython

git clone --depth 1 https://git.fslab.de/jkonra2m/tinydtls.git
cd tinydtls
autoreconf
./configure --with-ecc --without-debug
cd cython
sudo python3 setup.py install

cd ../..
git clone https://github.com/chrysn/aiocoap
cd aiocoap
git reset --hard 3286f48f0b949901c8b5c04c0719dc54ab63d431
sudo python3 -m pip install --upgrade pip setuptools
sudo python3 -m pip install .
```

# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/ggravlingen/pytradfri) project and adds a REST API for simpler usage.

## Installation
Tested on Raspbian (stretch) and LinuxMint (tessa)

```shell
sudo apt install python3-klein autoconf libtool
sudo pip3 install --upgrade pytradfri

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

### Login
First you'll need to login providing the IP of the gateway and the security code (written on the back):

```shell
curl --request POST \
  --url http://localhost:2080/login \
  --header 'content-type: application/json' \
  --data '{
    "host": "192.168.0.7",
    "code": "0RfPG338tTwBthto"
}'
```

The response will contain a authorization token:
```json
{ "token": "eyJob3N0IjogIjE3Mi4..." }
```

Use this in the header for all other requests:
```
authorization: Bearer eyJob3N0IjogIjE3Mi4...
```

### List all devices
```shell
curl --request GET \
  --url http://localhost:2080/devices \
  --header 'authorization: Bearer XXX'
```

### Turn light/socket on/off
Use the `id` of the device and state can be either `0` or `1`

```shell
curl --request PUT \
  --url http://localhost:2080/devices/65545/state/1 \
  --header 'authorization: Bearer XXX'
```

### Change light dimmer
Use the `id` of the device and dimmer can be any value between `0` or `254`

```shell
curl --request PUT \
  --url http://localhost:2080/devices/65545/dimmer/254 \
  --header 'authorization: Bearer XXX'
```

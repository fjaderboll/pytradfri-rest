# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/home-assistant-libs/pytradfri) project and adds a REST API for simpler usage of controlling your IKEA lights.

## Setup
Below is tested on Raspbian (stretch) and LinuxMint (tessa), but should work in all similar environments.

### With docker
Install Docker first if you haven't:
```shell
sudo apt install docker-ce   # Raspbian
sudo apt install docker.io   # other
```

Then run:
```shell
./docker/build.sh      # builds the image
./docker/run.sh 2080   # starts server at http://localhost:2080/
```

### Without docker
First time only:
```shell
sudo ./docker/install-coap-client.sh
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Run:
```shell
source .venv/bin/activate
./rest.py 2080         # starts server at http://localhost:2080/
```

## Usage

### Login
First you'll need to login providing the IP of the gateway and the security code (written on the back of the gateway):

```shell
curl --request POST \
  --url http://localhost:2080/login \
  --header 'content-type: application/json' \
  --data '{ "host": "192.168.0.7", "code": "0RfPG338tTwBthto" }'
```

The response will contain a authorization token:
```json
{ "token": "ZXCWeWiPfYhki..." }
```

Use this in the header for all other requests, like this:

```shell
curl -X GET --header 'authorization: Bearer ZXCWeWiPfYhki...' http://localhost:2080/devices
curl -X PUT --header 'authorization: Bearer ZXCWeWiPfYhki...' http://localhost:2080/devices/65545/state/1
```

This token does never expire.

### List all devices/groups
```shell
GET /devices
GET /groups
```

### Get single device/group
Use the `id` property of the device/group from above response

```shell
GET /devices/65545
GET /groups/131077
```

### Turn light/socket on/off
**state** can be either `0` or `1`. When used on a group it's applied to all applicable devices.

```shell
PUT /devices/65545/state/1
PUT /groups/131077/state/0
```

### Change light dimmer
**dimmer** can be any value between `0` or `254`. When used on a group it's applied to all applicable devices.
It's also possible to add a transition time. **transition** is a positive decimal number in seconds.

```shell
PUT /devices/65545/dimmer/254
PUT /groups/131077/dimmer/50

PUT /devices/65545/dimmer/254/transition/0.75
PUT /groups/131077/dimmer/50/transition/3
```

### Change blind position
**blind** can be any value between `0` or `100` (I think, untested!)

```shell
PUT /devices/65545/blind/50
```

### Get group devices with details
```shell
GET /groups/131077/devices
```

### Get gateway information
```shell
GET /gateway
```

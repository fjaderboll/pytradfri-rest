# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/home-assistant-libs/pytradfri)
project and adds a REST API for simpler usage of controlling your IKEA lights.

## Examples
```shell
GET /devices                 # retrieve all devices
GET /groups                  # retrieve all groups
GET /devices/65545           # get single device information
PUT /devices/65545/state/1   # turn device on
PUT /devices/65545/state/0   # turn device off
PUT /groups/131077/dimmer/60 # dim all lamps in group to 60%
PUT /gateway/restart         # restart gateway
```

Use **Swagger UI** to view all available endpoints.

## Setup
Below is tested on Raspbian (stretch) and Linux Mint 20.3 (Una),
but should work in all similar environments.

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

### Without docker (development)
First time only:
```shell
sudo ./docker/install-coap-client.sh
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Run:
```shell
source .venv/bin/activate
./rest/rest.py 2080    # start server at http://localhost:2080/
```

## Usage
Navigate to [http://localhost:2080/](http://localhost:2080/) to view the
**Swagger UI** and all available endpoints.

### Login
First you'll need to login providing the IP of the gateway and the security
code (written on the back of the gateway):

```shell
curl --request POST \
  --url http://localhost:2080/gateway/login \
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

This token does never expire, but keep in mind it's linked to your IKEA gateway
IP, so using a static IP might be a good idea.

# Known issues

* Setting dimmer value on a group will not turn on lights who already have that exact value since earlier. This works on individual devices.

# Upgrade requirements

```shell
pip3 install pip-upgrader
pip-upgrade
```

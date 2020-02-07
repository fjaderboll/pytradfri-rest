# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/ggravlingen/pytradfri) project and adds a REST API for simpler usage of controlling your IKEA lights.

## Setup
Below is tested on Raspbian (stretch) and LinuxMint (tessa), but should work in all similar environments.

### Docker
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

### Installation (without docker)
```shell
sudo ./docker/setup.sh   # installs all dependencies
./rest.py 2080           # starts server at http://localhost:2080/
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
{ "token": "eyJob3N0IjogIjE3Mi4..." }
```

Use this in the header for all other requests:
```
authorization: Bearer eyJob3N0IjogIjE3Mi4...
```
This token does never expire.

### List all devices/groups
```shell
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/devices
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/groups
```

### Get single device/group
Use the `id` property of the device/group from above response

```shell
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/devices/65545
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/groups/131077
```

### Turn light/socket on/off
`state` can be either `0` or `1`

```shell
curl -X PUT --header 'authorization: Bearer XXX' http://localhost:2080/devices/65545/state/1
curl -X PUT --header 'authorization: Bearer XXX' http://localhost:2080/groups/131077/state/0
```

### Change light dimmer
`dimmer` can be any value between `0` or `254`

```shell
curl -X PUT --header 'authorization: Bearer XXX' http://localhost:2080/devices/65545/dimmer/254
curl -X PUT --header 'authorization: Bearer XXX' http://localhost:2080/groups/131077/dimmer/50
```

### Change blind position
`blind` can be any value between `0` or `100` (I think, untested!)

```shell
curl -X PUT --header 'authorization: Bearer XXX' http://localhost:2080/devices/65545/blind/50
```

### Get group devices with details
```shell
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/groups/131077/devices
```

### Get gateway information
```shell
curl -X GET --header 'authorization: Bearer XXX' http://localhost:2080/gateway
```

# IKEA Trådfri - REST API
This is built on the [pytradfri](https://github.com/home-assistant-libs/pytradfri)
project and adds a REST API for simpler usage of controlling your IKEA lights.

> [!TIP]
> If you're using the new *IKEA Dirigera Hub*
> (which has Matter support), check out my other project
> [matter-rest](https://github.com/fjaderboll/matter-rest).


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

Use *Swagger UI* to view all available endpoints.

## Quick start
```shell
docker run -d --restart unless-stopped --name pytradfri-rest -p 2080:80 ghcr.io/fjaderboll/pytradfri-rest
```

## Development setup
If you want to build yourself (eg for Raspbian) or do local development,
see [development.md](docs/development.md) for details.

## Usage
Navigate to [http://localhost:2080/](http://localhost:2080/) to view the
*Swagger UI* and all available endpoints.

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

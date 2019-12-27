#!/usr/bin/env python3

# Hack to allow relative import above top level package
import sys
import os
folder = os.path.dirname(os.path.abspath(__file__))  # noqa
sys.path.insert(0, os.path.normpath("%s/.." % folder))  # noqa

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

import uuid
import threading
import time
import json
import base64

from klein import run, route

"""
Request POST body:
{
    "host": "192.168.0.1",
    "code": "aabbccddeeff1234"
}
Response body:
{
  "auth": "eyJob3N0IjogIjE4Mi4xNi4xLjkuLCAiaWRlbnRpdHkiOiAiY2Q1ZTVhZGIzNWZhNDAwNjayYzAzZjM0NjgyYTE3YTgiLCAicHNrIjogIkI4Umt1ak1zNDhxTjNTZ1UifQ=="
}
"""
@route('/login')
def login(request, methods=['POST']):
    raw_data = request.content.read().decode("utf-8")
    data = json.loads(raw_data)

    identity = uuid.uuid4().hex
    api_factory = APIFactory(host=data['host'], psk_id=identity)
    psk = api_factory.generate_psk(data['code'])

    login_data = {
        'host': data['host'],
        'identity': identity,
        'psk': psk
    }
    auth = {
        'authentication': base64.b64encode(json.dumps(login_data).encode()).decode("utf-8")
    }
    return json.dumps(auth)

def get_gateway_api(request):
    auth = request.getHeader('Authorization')
    token = auth.split(' ')[1]
    raw_login_data = base64.b64decode(token)
    login_data = json.loads(raw_login_data)

    api_factory = APIFactory(host=login_data['host'], psk_id=login_data['identity'], psk=login_data['psk'])
    api = api_factory.request
    gateway = Gateway()

    return (gateway, api)

@route('/devices')
def devices(request, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    items = []
    for device in devices:
        item = {
            'id': device.id,
            'name': device.name,
            'type': 'unknown',
            'typeId': device.application_type,
            'reachable': device.reachable,
            'lastSeen': str(device.last_seen),
            'info': {
                'manufacturer': device.device_info.manufacturer,
                'modelNumber': device.device_info.model_number,
                'serial': device.device_info.serial,
                'firmwareVersion': device.device_info.firmware_version,
                'powerSource': device.device_info.power_source_str,
                'powerSourceId': device.device_info.power_source,
                'batteryLevel': device.device_info.battery_level
            }
        }

        if device.has_light_control:
            item['type'] = 'light'
            item['state'] = device.light_control.lights[0].state
            item['dimmer'] = device.light_control.lights[0].dimmer

        if device.has_blind_control:
            item['type'] = 'blind'
            item['state'] = device.blind_control.blinds[0].current_cover_position

        if device.has_socket_control:
            item['type'] = 'socket'
            item['state'] = device.socket_control.sockets[0].state

        if device.has_signal_repeater_control:
            item['type'] = 'repeater'

        items.append(item)
    return json.dumps(items)

@route('/devices/<int:id>/state/<int:state>')
def device_dimmer(request, id, state, methods=['PUT']):
    (gateway, api) = get_gateway_api(request)

    device_command = gateway.get_device(id)
    device = api(device_command)

    if device.has_light_control or device.has_socket_control:
        state_command = device.light_control.set_state(state != 0)
        api(state_command)
    else:
        raise Exception('Invalid device type for this operation')

@route('/devices/<int:id>/dimmer/<int:dimmer>')
def device_state(request, id, dimmer, methods=['PUT']):
    (gateway, api) = get_gateway_api(request)

    device_command = gateway.get_device(id)
    device = api(device_command)

    if device.has_light_control or device.has_socket_control:
        dim_command = device.light_control.set_dimmer(dimmer)
        api(dim_command)
    else:
        raise Exception('Invalid device type for this operation')

if __name__ == '__main__':
    port = 80
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    run("0.0.0.0", port)

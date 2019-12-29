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

APP_TYPES = [
    'remote',
    'unknown', # TODO blind?
    'light',
    'socket'
]

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
    # TODO better/safer way of handling this information
    auth = {
        'token': base64.b64encode(json.dumps(login_data).encode()).decode("utf-8")
    }
    return json.dumps(auth)

def get_gateway_api(request):
    auth = request.getHeader('authorization')
    token = auth.split(' ')[1]
    raw_login_data = base64.b64decode(token).decode("utf-8")
    login_data = json.loads(raw_login_data)

    api_factory = APIFactory(host=login_data['host'], psk_id=login_data['identity'], psk=login_data['psk'])
    api = api_factory.request
    gateway = Gateway()

    return (gateway, api)

def get_device(request, id):
    (gateway, api) = get_gateway_api(request)

    device_command = gateway.get_device(id)
    device = api(device_command)
    return (device, api)

def get_device_item(device):
    item = {
        'id': device.id,
        'name': device.name,
        'type': (APP_TYPES[device.application_type] if device.application_type < len(APP_TYPES) else 'unknown'),
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
        item['state'] = device.light_control.lights[0].state
        item['dimmer'] = device.light_control.lights[0].dimmer

    if device.has_blind_control:
        item['state'] = device.blind_control.blinds[0].current_cover_position

    if device.has_socket_control:
        item['state'] = device.socket_control.sockets[0].state

    if device.has_signal_repeater_control:
        pass

    return item

@route('/gateway')
def gateway(request, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    gateway_command = gateway.get_gateway_info()
    gateway_info = api(gateway_command)

    return json.dumps({
        'id': gateway_info.id,
        'ntpServer': gateway_info.ntp_server,
        'firmwareVersion': gateway_info.firmware_version,
        'currentTime': str(gateway_info.current_time),
        'currentTimeIso8601': gateway_info.current_time_iso8601,
        'firstSetup': str(gateway_info.first_setup),
        'homekitId': gateway_info.homekit_id
    })

@route('/devices')
def devices(request, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    items = []
    for device in devices:
        item = get_device_item(device)
        items.append(item)
    return json.dumps(items)

@route('/devices/<int:id>')
def device(request, id, methods=['GET']):
    (device, api) = get_device(request, id)
    item = get_device_item(device)
    return json.dumps(item)

@route('/devices/<int:id>/state/<int:state>')
def device_state(request, id, state, methods=['PUT']):
    (device, api) = get_device(request, id)

    if device.has_light_control:
        state_command = device.light_control.set_state(state != 0)
        api(state_command)
    elif device.has_socket_control:
        state_command = device.socket_control.set_state(state != 0)
        api(state_command)
    else:
        raise Exception('Invalid device type for this operation')

@route('/devices/<int:id>/dimmer/<int:dimmer>')
def device_dimmer(request, id, dimmer, methods=['PUT']):
    (device, api) = get_device(request, id)

    if device.has_light_control:
        dim_command = device.light_control.set_dimmer(dimmer)
        api(dim_command)
    else:
        raise Exception('Invalid device type for this operation')

@route('/devices/<int:id>/blind/<int:state>')
def device_blind(request, id, state, methods=['PUT']):
    (device, api) = get_device(request, id)

    if device.has_blind_control:
        state_command = device.blind_control.set_state(state)
        api(state_command)
    else:
        raise Exception('Invalid device type for this operation')

def get_group_item(group):
    item = {
        'id': group.id,
        'name': group.name,
        'deviceIds': group.member_ids
    }
    return item

@route('/groups')
def groups(request, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    groups_command = gateway.get_groups()
    groups_commands = api(groups_command)
    groups = api(groups_commands)

    items = []
    for group in groups:
        item = get_group_item(group)
        items.append(item)
    return json.dumps(items)

@route('/groups/<int:id>')
def group(request, id, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    group_command = gateway.get_group(id)
    group = api(group_command)

    item = get_group_item(group)
    return json.dumps(item)

@route('/groups/<int:id>/devices')
def group_devices(request, id, methods=['GET']):
    (gateway, api) = get_gateway_api(request)

    group_command = gateway.get_group(id)
    group = api(group_command)

    items = []
    for member_id in group.member_ids:
        device_command = gateway.get_device(member_id)
        device = api(device_command)
        item = get_device_item(device)
        items.append(item)
    return json.dumps(items)

if __name__ == '__main__':
    port = 80
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    run("0.0.0.0", port)

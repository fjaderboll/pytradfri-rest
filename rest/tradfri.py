
from flask import request, abort

from pytradfri import Gateway
from pytradfri import const
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError, RequestTimeout
from pytradfri.util import load_json, save_json

import uuid
import string

import utils

APP_TYPES = [
    'remote',
    'unknown', # TODO blind?
    'light',
    'socket'
]

def get_gateway_api():
    try:
        auth = request.headers.get('authorization')
        token = auth.split(' ')[1]
        login_data = utils.decrypt(token)
        (host, identity, psk) = login_data.split(',')

        api_factory = APIFactory(host=host, psk_id=identity, psk=psk)
        api = api_factory.request
        gateway = Gateway()

        return (gateway, api)
    except:
        abort(401, 'Not authorized')

def get_device_api(id):
    (gateway, api) = get_gateway_api()

    device_command = gateway.get_device(id)
    device = api(device_command)
    if device.raw is None:
        abort(404, 'Device not found')
    return (device, api)

def get_group_api(id):
    (gateway, api) = get_gateway_api()

    group_command = gateway.get_group(id)
    group = api(group_command)
    if group.raw is None:
        abort(404, 'Group not found')

    return (group, api)

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

def get_group_item(group):
    item = {
        'id': group.id,
        'name': group.name,
        'deviceIds': group.member_ids
    }
    return item

def login(data):
    if len(data['code']) != 16:
        abort(400, 'Invalid security code')

    identity = uuid.uuid4().hex
    api_factory = APIFactory(host=data['host'], psk_id=identity)
    try:
        psk = api_factory.generate_psk(data['code'])
    except RequestTimeout:
        abort(401, 'Unable to complete authentication')

    login_data = data['host'] + ',' + identity + ',' + psk
    return {
        'token': utils.encrypt(login_data)
    }

def get_gateway_info():
    (gateway, api) = get_gateway_api()

    gateway_command = gateway.get_gateway_info()
    gateway_info = api(gateway_command)

    return {
        'id': gateway_info.id,
        'ntpServer': gateway_info.ntp_server,
        'firmwareVersion': gateway_info.firmware_version,
        'currentTime': str(gateway_info.current_time),
        'currentTimeIso8601': gateway_info.current_time_iso8601,
        'firstSetupTime': str(gateway_info.first_setup),
        'homekitId': gateway_info.homekit_id,
        'pairStatusGoogleHome': gateway_info.pair_status_google_home,
        'pairStatusAlexa': gateway_info.pair_status_alexa
    }

def restart_gateway():
    (gateway, api) = get_gateway_api()

    gateway_command = gateway.reboot()
    gateway_restart = api(gateway_command)

    return {}

def get_devices():
    (gateway, api) = get_gateway_api()

    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    items = []
    for device in devices:
        item = get_device_item(device)
        items.append(item)
    return items

def get_device(id):
    (device, api) = get_device_api(id)
    return get_device_item(device)

def get_transition_value(transition):
    return None if transition is None else int(transition*10)

def get_dimmer_value(dimmer):
    if dimmer < 0 or 100 < dimmer:
        abort(400, 'Dimmer value must be between 0 and 100')
    return int(dimmer/100.0*254)

def get_colortemp_value(colortemp):
    if colortemp < 0 or 100 < colortemp:
        abort(400, 'Color temperature value must be between 0 and 100')
    inverted = 100 - colortemp
    max = 454
    min = 250
    return min + int((max - min) * inverted/100.0)

def set_device_state(id, state):
    (device, api) = get_device_api(id)

    if device.has_light_control:
        state_command = device.light_control.set_state(state != 0)
        api(state_command)
    elif device.has_socket_control:
        state_command = device.socket_control.set_state(state != 0)
        api(state_command)
    else:
        abort(400, 'Invalid device type for this operation')

def set_device_dimmer(id, dimmer, transition):
    (device, api) = get_device_api(id)

    if device.has_light_control:
        dimmer_value = get_dimmer_value(dimmer)
        transition_value = get_transition_value(transition)
        dim_command = device.light_control.set_dimmer(dimmer_value, transition_time=transition_value)
        api(dim_command)
    else:
        abort(400, 'Unsupported operation for this device')

def set_device_color(id, color, transition):
    (device, api) = get_device_api(id)

    if len(color) != 6 or not all(c in string.hexdigits for c in color):
        abort(400, 'Invalid HEX color')

    if device.has_light_control: # and device.light_control.can_set_color:
        transition_value = get_transition_value(transition)
        color_command = device.light_control.set_hex_color(color, transition_time=transition_value)
        api(color_command)
    else:
        abort(400, 'Unsupported operation for this device')

def set_device_colortemp(id, colortemp, transition):
    (device, api) = get_device_api(id)

    if device.has_light_control: # and device.light_control.can_set_temp:
        colortemp_value = get_colortemp_value(colortemp)
        transition_value = get_transition_value(transition)
        colortemp_command = device.light_control.set_color_temp(colortemp_value, transition_time=transition_value)
        api(colortemp_command)
    else:
        abort(400, 'Unsupported operation for this device')

def set_device_blind(id, state):
    (device, api) = get_device_api(id)

    if device.has_blind_control:
        state_command = device.blind_control.set_state(state)
        api(state_command)
    else:
        abort(400, 'Unsupported operation for this device')

def get_groups():
    (gateway, api) = get_gateway_api()

    groups_command = gateway.get_groups()
    groups_commands = api(groups_command)
    groups = api(groups_commands)

    items = []
    for group in groups:
        item = get_group_item(group)
        items.append(item)
    return items

def get_group(id):
    (group, api) = get_group_api(id)
    return get_group_item(group)

def get_group_devices(id):
    (gateway, api) = get_gateway_api()

    group_command = gateway.get_group(id)
    group = api(group_command)

    items = []
    for member_id in group.member_ids:
        device_command = gateway.get_device(member_id)
        device = api(device_command)
        item = get_device_item(device)
        items.append(item)
    return items

def set_group_state(id, state):
    (group, api) = get_group_api(id)

    state_command = group.set_state(state != 0)
    api(state_command)

def set_group_dimmer(id, dimmer, transition):
    (group, api) = get_group_api(id)

    dimmer_value = get_dimmer_value(dimmer)
    transition_value = get_transition_value(transition)
    dim_command = group.set_dimmer(dimmer_value, transition_time=transition_value)
    api(dim_command)

def set_group_color(id, color, transition):
    (group, api) = get_group_api(id)

    if len(color) != 6 or not all(c in string.hexdigits for c in color):
        abort(400, 'Invalid HEX color')

    transition_value = get_transition_value(transition)
    color_command = group.set_hex_color(color, transition_time=transition_value)
    api(color_command)

def set_group_colortemp(id, colortemp, transition):
    (group, api) = get_group_api(id)

    colortemp_value = get_colortemp_value(colortemp)
    transition_value = get_transition_value(transition)
    colortemp_command = group.set_color_temp(colortemp_value, transition_time=transition_value)
    api(colortemp_command)

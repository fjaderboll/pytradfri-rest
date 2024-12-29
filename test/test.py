#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import requests
import random
import time

def check_response(response, name):
	print(f'{response.request.method} {response.request.url}: {response.status_code} {response.text}')
	response.raise_for_status()

def login():
	headers = {
		'content-type': 'application/json'
	}
	data = {
		'host': args.host,
		'code': args.code
	}
	response = requests.post(f'{args.url}/gateway/login', headers=headers, data=json.dumps(data))
	check_response(response, 'Login')
	return response.json()['token']

def test_endpoint(method, endpoint, headers, delay=0.5):
	time.sleep(delay)

	url = f'{args.url}{endpoint}'
	if method == 'GET':
		response = requests.get(url, headers=headers)
		check_response(response, endpoint)
		return response.json()
	elif method == 'PUT':
		response = requests.put(url, headers=headers)
		check_response(response, endpoint)
		return response.text
	else:
		raise ValueError(f'Unknown method: {method}')
	

def get_random_item(items, filterFunc=None):
	if filterFunc:
		items = list(filter(filterFunc, items))
	if len(items) == 0:
		return None
	return items[random.randint(0, len(items) - 1)]

def parseargs():
	parser = argparse.ArgumentParser(description='Test endpoints')
	parser.add_argument('--host', help='IP of gateway (required if no token provided)')
	parser.add_argument('--code', help='Code of gateway (required if no token provided)')
	parser.add_argument('--token', help='Token (instead of host and code)')
	parser.add_argument('--url', help='URL, default "http://localhost:2080"', default='http://localhost:2080')
	args = parser.parse_args()
	return args

if __name__ == '__main__':
	print('Testing endpoints')
	print('-----------------')

	args = parseargs()
	
	if not args.token:
		token = login()
	else:
		token = args.token
	headers = { 'authorization': 'Bearer ' + token }

	test_endpoint('GET', '/gateway/', headers)
	
	devices = test_endpoint('GET', '/devices/', headers)
	device = test_endpoint('GET', f'/devices/{get_random_item(devices)["id"]}', headers)

	random_light = get_random_item(devices, lambda x: x['type'] == 'light')
	if random_light:
		print(random_light)
		test_endpoint('PUT', f'/devices/{random_light["id"]}/state/0', headers)
		test_endpoint('PUT', f'/devices/{random_light["id"]}/state/1', headers)
	
	random_dimmer = get_random_item(devices, lambda x: 'dimmer' in x)
	if random_dimmer:
		print(random_dimmer)
		test_endpoint('PUT', f'/devices/{random_dimmer["id"]}/dimmer/0', headers)
		test_endpoint('PUT', f'/devices/{random_dimmer["id"]}/dimmer/100', headers)
		test_endpoint('PUT', f'/devices/{random_dimmer["id"]}/dimmer/0/transition/2', headers)
		test_endpoint('PUT', f'/devices/{random_dimmer["id"]}/dimmer/100/transition/1', headers, delay=2)

	groups = test_endpoint('GET', '/groups/', headers, delay=2)
	group = test_endpoint('GET', f'/groups/{get_random_item(groups)["id"]}', headers)
	group_devices = test_endpoint('GET', f'/groups/{get_random_item(groups)["id"]}/devices', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/state/0', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/state/1', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/dimmer/0', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/dimmer/100', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/dimmer/0/transition/2', headers)
	test_endpoint('PUT', f'/groups/{group["id"]}/dimmer/100/transition/1', headers, delay=2)

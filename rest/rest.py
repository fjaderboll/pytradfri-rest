#!/usr/bin/env python3

import sys
from flask import Flask, Blueprint

from api import api
from endpoints.gateway import ns as namespace_gateway
from endpoints.devices import ns as namespace_devices
from endpoints.groups import ns as namespace_groups

app = Flask(__name__)

def main(port, debug):
    blueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(blueprint)
    api.add_namespace(namespace_gateway)
    api.add_namespace(namespace_devices)
    api.add_namespace(namespace_groups)
    app.register_blueprint(blueprint)
    app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == '__main__':
    port = 80
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    main(port, port != 80)

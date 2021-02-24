
from flask_restplus import Resource, fields

from api import api
import tradfri

ns = api.namespace('devices', description='Device information and control')

@ns.route('/')
class DeviceList(Resource):
    def get(self):
        return tradfri.get_devices()

@ns.route('/<int:id>')
@ns.param('id', 'The id of the device')
@ns.response(404, 'Unknown device')
class DeviceGet(Resource):
    def get(self, id):
        return tradfri.get_device(id)

@ns.route('/<int:id>/state/<int:state>')
class DeviceState(Resource):
    def put(self, id, state):
        tradfri.set_device_state(id, state)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<float:transition>')
@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<int:transition>')
class DeviceDimmerTransition(Resource):
    def put(self, id, dimmer, transition):
        tradfri.set_device_dimmer(id, dimmer, transition)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>')
class DeviceDimmer(Resource):
    def put(self, id, dimmer):
        tradfri.set_device_dimmer(id, dimmer, None)
        return None, 204

@ns.route('/<int:id>/blind/<int:state>')
class DeviceBlind(Resource):
    def put(self, id, state):
        tradfri.set_device_blind(id, state)
        return None, 204

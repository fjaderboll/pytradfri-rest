
from flask_restplus import Resource, fields

from api import api
import tradfri

ns = api.namespace('devices', description='Device information and control')

@ns.route('/')
class DeviceList(Resource):
    def get(self):
        return tradfri.get_devices()

@ns.route('/<int:id>')
@ns.param('id', 'Device id')
class DeviceGet(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Unknown device')
    def get(self, id):
        return tradfri.get_device(id)

@ns.route('/<int:id>/state/<int:state>')
@ns.param('state', '0 for off and 1 for on')
@ns.param('id', 'Device id')
class DeviceState(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Invalid device type for this operation')
    @ns.response(404, 'Unknown device')
    def put(self, id, state):
        tradfri.set_device_state(id, state)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<float:transition>')
@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<int:transition>')
@ns.param('transition', 'Transition time in seconds, decimals allowed')
@ns.param('dimmer', 'Dim value in percent, 0 for off and 100 for max brightness')
@ns.param('id', 'Device id')
class DeviceDimmerTransition(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Invalid device type for this operation')
    @ns.response(404, 'Unknown device')
    def put(self, id, dimmer, transition):
        tradfri.set_device_dimmer(id, dimmer, transition)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>')
@ns.param('dimmer', 'Dim value in percent, 0 for off and 100 for max brightness')
@ns.param('id', 'Device id')
class DeviceDimmer(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Invalid device type for this operation')
    @ns.response(404, 'Unknown device')
    def put(self, id, dimmer):
        tradfri.set_device_dimmer(id, dimmer, None)
        return None, 204

@ns.route('/<int:id>/blind/<int:state>')
@ns.param('id', 'Device id')
class DeviceBlind(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Invalid device type for this operation')
    @ns.response(404, 'Unknown device')
    def put(self, id, state):
        tradfri.set_device_blind(id, state)
        return None, 204

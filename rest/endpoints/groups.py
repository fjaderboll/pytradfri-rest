
from flask_restplus import Resource, fields

from api import api
import tradfri

ns = api.namespace('groups', description='Group information and control')

@ns.route('/')
class GroupList(Resource):
    def get(self):
        return tradfri.get_groups()

@ns.route('/<int:id>')
@ns.param('id', 'Group id')
@ns.response(404, 'Unknown group')
class GroupGet(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Unknown group')
    def get(self, id):
        return tradfri.get_group(id)

@ns.route('/<int:id>/devices')
@ns.param('id', 'Group id')
@ns.response(404, 'Unknown group')
class GroupGetDevices(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Unknown group')
    def get(self, id):
        return tradfri.get_group_devices(id)

@ns.route('/<int:id>/state/<int:state>')
@ns.param('state', '0 for off and 1 for on')
@ns.param('id', 'Group id')
class GroupState(Resource):
    @ns.response(204, 'Success')
    @ns.response(404, 'Unknown group')
    def put(self, id, state):
        tradfri.set_group_state(id, state)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<float:transition>')
@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<int:transition>')
@ns.param('transition', 'Transition time in seconds, decimals allowed')
@ns.param('dimmer', 'Dim value in percent, 0 for off and 100 for max brightness')
@ns.param('id', 'Group id')
class GroupDimmerTransition(Resource):
    @ns.response(204, 'Success')
    @ns.response(404, 'Unknown group')
    def put(self, id, dimmer, transition):
        tradfri.set_group_dimmer(id, dimmer, transition)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>')
@ns.param('dimmer', 'Dim value in percent, 0 for off and 100 for max brightness')
@ns.param('id', 'Group id')
class GroupDimmer(Resource):
    @ns.response(204, 'Success')
    @ns.response(404, 'Unknown group')
    def put(self, id, dimmer):
        tradfri.set_group_dimmer(id, dimmer, None)
        return None, 204

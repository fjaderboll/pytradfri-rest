
from flask_restx import Resource, fields

from api import api
import tradfri

ns = api.namespace('groups', description='Group information and control')

@ns.route('/')
class GroupList(Resource):
    def get(self):
        return tradfri.get_groups()

@ns.route('/<int:id>')
@ns.param('id', 'Group id, eg 131085')
@ns.response(404, 'Unknown group')
class GroupGet(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Unknown group')
    def get(self, id):
        return tradfri.get_group(id)

@ns.route('/<int:id>/devices')
@ns.param('id', 'Group id, eg 131085')
@ns.response(404, 'Unknown group')
class GroupGetDevices(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Unknown group')
    def get(self, id):
        return tradfri.get_group_devices(id)

@ns.route('/<int:id>/state/<int:state>')
@ns.param('state', '0 for off and 1 for on')
@ns.param('id', 'Group id, eg 131085')
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
@ns.param('id', 'Group id, eg 131085')
class GroupDimmerTransition(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Bad request')
    @ns.response(404, 'Unknown group')
    def put(self, id, dimmer, transition):
        tradfri.set_group_dimmer(id, dimmer, transition)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>')
@ns.param('dimmer', 'Dim value in percent, 0 for off and 100 for max brightness')
@ns.param('id', 'Group id, eg 131085')
class GroupDimmer(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Bad request')
    @ns.response(404, 'Unknown group')
    def put(self, id, dimmer):
        tradfri.set_group_dimmer(id, dimmer, None)
        return None, 204

@ns.route('/<int:id>/color/<string:color>/transition/<float:transition>')
@ns.route('/<int:id>/color/<string:color>/transition/<int:transition>')
@ns.param('transition', 'Transition time in seconds, decimals allowed')
@ns.param('color', 'Hex code, eg aa0055')
@ns.param('id', 'Group id, eg 131085')
class GroupDimmerTransition(Resource):
    @ns.response(204, 'Success')
    @ns.response(404, 'Unknown group')
    def put(self, id, color, transition):
        tradfri.set_group_color(id, color, transition)
        return None, 204

@ns.route('/<int:id>/color/<string:color>')
@ns.param('color', 'Hex code, eg aa0055')
@ns.param('id', 'Group id, eg 131085')
class GroupDimmer(Resource):
    @ns.response(204, 'Success')
    @ns.response(404, 'Unknown group')
    def put(self, id, color):
        tradfri.set_group_color(id, color, None)
        return None, 204

@ns.route('/<int:id>/colortemp/<int:colortemp>/transition/<float:transition>')
@ns.route('/<int:id>/colortemp/<int:colortemp>/transition/<int:transition>')
@ns.param('transition', 'Transition time in seconds, decimals allowed')
@ns.param('colortemp', 'Color temperature in percent, 0 for warm and 100 for white')
@ns.param('id', 'Group id, eg 131085')
class GroupDimmerTransition(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Bad request')
    @ns.response(404, 'Unknown group')
    def put(self, id, colortemp, transition):
        tradfri.set_group_colortemp(id, colortemp, transition)
        return None, 204

@ns.route('/<int:id>/colortemp/<int:colortemp>')
@ns.param('colortemp', 'Color temperature in percent, 0 for warm and 100 for white')
@ns.param('id', 'Group id, eg 131085')
class GroupDimmer(Resource):
    @ns.response(204, 'Success')
    @ns.response(400, 'Bad request')
    @ns.response(404, 'Unknown group')
    def put(self, id, colortemp):
        tradfri.set_group_colortemp(id, colortemp, None)
        return None, 204

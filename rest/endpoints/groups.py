
from flask_restplus import Resource, fields

from api import api
import tradfri

ns = api.namespace('groups', description='Group information and control')

@ns.route('/')
class GroupList(Resource):
    def get(self):
        return tradfri.get_groups()

@ns.route('/<int:id>')
@ns.param('id', 'The id of the group')
@ns.response(404, 'Unknown group')
class GroupGet(Resource):
    def get(self, id):
        return tradfri.get_group(id)

@ns.route('/<int:id>/devices')
@ns.param('id', 'The id of the group')
@ns.response(404, 'Unknown group')
class GroupGetDevices(Resource):
    def get(self, id):
        return tradfri.get_group_devices(id)

@ns.route('/<int:id>/state/<int:state>')
class GroupState(Resource):
    def put(self, id, state):
        tradfri.set_group_state(id, state)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<float:transition>')
@ns.route('/<int:id>/dimmer/<int:dimmer>/transition/<int:transition>')
class GroupDimmerTransition(Resource):
    def put(self, id, dimmer, transition):
        tradfri.set_group_dimmer(id, dimmer, transition)
        return None, 204

@ns.route('/<int:id>/dimmer/<int:dimmer>')
class GroupDimmer(Resource):
    def put(self, id, dimmer):
        tradfri.set_group_dimmer(id, dimmer, None)
        return None, 204

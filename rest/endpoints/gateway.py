
from flask_restplus import Resource, fields

from api import api
import tradfri

ns = api.namespace('gateway', description='Gateway information and authentication')

@ns.route('/')
class GatewayInfo(Resource):

    def get(self):
        return tradfri.get_gateway_info()

@ns.route('/login')
class GatewayLogin(Resource):
    post_fields = api.model('LoginData', {
        'host': fields.String,
        'code': fields.String
    })

    @api.doc(security=None)
    @api.expect(post_fields, validate=True)
    def post(self):
        return tradfri.login(api.payload)


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
        'host': fields.String(description='Gateway address, eg 192.168.0.7', required=True),
        'code': fields.String(description='Gateway security code, eg 0RfPG338tTwBthto', required=True)
    })

    @api.doc(security=None)
    @api.expect(post_fields, validate=True)
    @ns.response(200, 'Success')
    @ns.response(401, 'Unable to complete authentication')
    def post(self):
        return tradfri.login(api.payload)

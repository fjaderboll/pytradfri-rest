
from flask_restplus import Api

authorizations = {
    'default': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='2.0',
            title='pytradfri-rest',
            description='A REST API for your IKEA Tradfri Gateway',
            authorizations=authorizations,
            security='default')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500

__author__ = 'kent'


from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

#TODO: Put this in a config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# TODO: Figure out exception handling better...
# errors = {
#     'ValueError': {
#         'message': 'Value was an invalid type',
#         'status': 400
#     }
# }

# api = restful.Api(app, errors=errors)
api = restful.Api(app)
db = SQLAlchemy(app)

from controller import *

api.add_resource(Alive, '/alive')

api.add_resource(GetObject, '/getObject/<rfid>')
api.add_resource(Checkout, '/checkOut/<userid>/<toolid>')


api.add_resource(OpenDoor, '/openDoor/<userid>/<toolid>')
api.add_resource(ReportBroken, '/reportBroken/<userid>/<toolid>')
api.add_resource(ReportMissing, '/reportMissing/<userid>/<toolid>')
api.add_resource(DoorStatus, '/doorStatus/<userid>/<toolid>')
api.add_resource(Checkin, '/checkIn/<userid>/<toolid>')
api.add_resource(Events, '/events')


#api.add_resource(ReportError, '/error')

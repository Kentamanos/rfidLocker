__author__ = 'kent'

from application import db
from flask_restful import fields
from datetime import datetime

permissions = db.Table('permissions',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('tool_id', db.Integer, db.ForeignKey('tool.id')),
                       db.UniqueConstraint('user_id', 'tool_id', name='uix_permissions_user_tool')
                       )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid = db.Column(db.String(40), unique=True)
    name = db.Column(db.Text)

    tools = db.relationship('Tool', secondary=permissions, backref='users')

    def __init__(self, rfid, name):
        self.rfid = rfid
        self.name = name


tool_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'rfid': fields.String,
    'checked_out_by': fields.Integer,
    'broken': fields.Boolean,
    'missing': fields.Boolean,
}

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rfid': fields.String,
    'available': fields.Nested(tool_fields),
    'user_checked_out': fields.Nested(tool_fields),
    'others_checked_out': fields.Nested(tool_fields)
}

event_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'tool_id': fields.Integer,
    'message': fields.String,
    'event_time': fields.DateTime
}

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    rfid = db.Column(db.String(40), unique=True)
    checked_out_by = db.Column(db.Integer, nullable=True)
    broken = db.Column(db.Boolean)
    missing = db.Column(db.Boolean)
    door_number = db.Column(db.Integer)

    def __init__(self, name, description, rfid, broken, missing, door_number):
        self.name = name
        self.description = description
        self.rfid = rfid
        self.broken = broken
        self.missing = missing
        self.door_number = door_number

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('events', lazy='dynamic'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))
    tool = db.relationship('Tool', backref=db.backref('events', lazy='dynamic'))
    message = db.Column(db.Text)

    def __init__(self, user_id, tool_id, message, event_time=None):
        if event_time is None:
            self.event_time = datetime.utcnow()
        self.user_id = user_id
        self.tool_id = tool_id
        self.message = message



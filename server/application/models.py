__author__ = 'kent'

from application import db
from flask_restful import fields

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
    'checked_out_by': fields.Integer
}

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rfid': fields.String,
    'available': fields.Nested(tool_fields),
    'user_checked_out': fields.Nested(tool_fields),
    'others_checked_out': fields.Nested(tool_fields)
}

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    rfid = db.Column(db.String(40), unique=True)
    checked_out_by = db.Column(db.Integer, nullable=True)

    def __init__(self, name, description, rfid):
        self.name = name
        self.description = description
        self.rfid = rfid

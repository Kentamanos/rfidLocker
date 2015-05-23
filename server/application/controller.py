__author__ = 'kent'

from flask import abort, jsonify
from flask.ext import restful
from flask_restful import marshal_with, marshal
from models import User, Tool, user_fields, tool_fields

from application import db

class Alive(restful.Resource):
    def get(self):
        return True

class GetObject(restful.Resource):
    # @marshal_with(user_object_response)
    def get(self, rfid):
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:
            #Couldn't find a user with that RFID, see if it's a tool...
            tool = Tool.query.filter_by(rfid=rfid).first()
            if tool is None:
                abort(404)
            return {'tool': marshal(tool, tool_fields)}
        # Return a user
        user.user_checked_out = Tool.query.filter_by(checked_out_by=user.id).all()
        user.others_checked_out = Tool.query.filter(Tool.checked_out_by != user.id).filter(Tool.checked_out_by is not None).all()
        user.available = [tool for tool in user.tools if tool.checked_out_by is None]
        return {'user': marshal(user, user_fields)}

class Checkout(restful.Resource):
    def get(self, userid, toolid):
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)

        user = User.query.filter_by(id=user_id).first()
        tool = Tool.query.filter_by(id=tool_id).first()

        if tool.checked_out_by is not None:
            abort(400, 'Tool already checked out')

        t = next(tool for tool in user.tools if tool.id == tool_id)
        if t is None:
            abort(400)
        else:
            t.checked_out_by = user_id
            db.session.commit()
            return True




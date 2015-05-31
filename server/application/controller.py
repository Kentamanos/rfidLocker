__author__ = 'kent'

from flask import abort, jsonify, request
from flask.ext import restful
from flask_restful import marshal_with, marshal
from models import User, Tool, user_fields, tool_fields, Event, event_fields

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
            db.session.add(Event(None, tool.id, "Tool scan"))
            return {'tool': marshal(tool, tool_fields)}
        # Return a user
        user.user_checked_out = Tool.query.filter_by(checked_out_by=user.id).all()
        user.others_checked_out = Tool.query.filter(Tool.checked_out_by != user.id).filter(Tool.checked_out_by is not None).all()
        user.available = [tool for tool in user.tools if tool.checked_out_by is None]
        db.session.add(Event(user.id, None, "User scan"))
        return {'user': marshal(user, user_fields)}

class Checkout(restful.Resource):
    # This method updates the database so that user specified with userid checks out the tool specified by toolid

    def get(self, userid, toolid):
        # userid and toolid are parsed as integers, if they're not integers, a 500 status is returned
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)

        # user and tool are found in the database
        user = User.query.filter_by(id=user_id).first()
        tool = Tool.query.filter_by(id=tool_id).first()

        # if one or both of the id's are not found, return a 404
        if user is None or tool is None:
            abort(404)

        # if the tool being checked out is already checked out, return an error
        if tool.checked_out_by is not None:
            abort(400, 'Tool already checked out')

        # find the tool in the list of tools the user is allowed to check out
        t = next(tool for tool in user.tools if tool.id == tool_id)
        if t is None:
            # the tool wasn't in the list of tools the user is allowed to checkout, return am error
            abort(400)
        else:
            # update the tool to be checked out by the user
            t.checked_out_by = user_id
            db.session.add(Event(user_id, tool_id, "Check out"))
            db.session.commit()
            return True

class Checkin(restful.Resource):
    def get(self, userid, toolid):
        # userid and toolid are parsed as integers, if they're not integers, a 500 status is returned
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)
        # Get the tool
        tool = Tool.query.filter_by(id=tool_id).first()
        if tool is None:
            abort(500)
        tool.checked_out_by = None
        db.session.add(Event(user_id, tool_id, "Check in"))
        db.session.commit()
        return True

class ReportBroken(restful.Resource):

    def get(self, userid, toolid):
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)
        tool = Tool.query.filter_by(id=tool_id).first()
        if tool is None:
            abort(500)
        tool.broken = True
        db.session.add(Event(user_id, tool_id, "Report broken"))
        db.session.commit()
        return True


class ReportMissing(restful.Resource):
    def get(self, userid, toolid):
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)
        # TODO: Code to report missing
        db.session.add(Event(user_id, tool_id, "Report missing"))

class DoorStatus(restful.Resource):
    def get(self, userid, toolid):
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)

class OpenDoor(restful.Resource):
    def get(self, userid, toolid):
        # TODO: Figure out better exception handling
        try:
            user_id = int(userid)
            tool_id = int(toolid)
        except ValueError:
            abort(500)
        # TODO: Code for opening door...
        db.session.add(Event, user_id, tool_id, "Open door")

class Events(restful.Resource):
    def get(self):
        events = Event.query.all()
        return marshal(events, event_fields)

__author__ = 'kent'

from application import db
from application.models import User, Tool

db.drop_all()
db.create_all()

kent = User('0000996368', 'Kent Bowling')
gus = User('gusRfid', 'Gus')
db.session.add(kent)
db.session.add(gus)

domino = Tool('Domino', 'A kick ass German biscuit joiner', 'dominoRfid')
db.session.add(domino)

pendant = Tool('MultiCAM Pendant',
               "A delicate CNC router pendant that could have its laser and dry run buttons frickin' labeled", 'multiCamRfid')
db.session.add(pendant)

db.session.commit()

kent.tools.append(domino)
kent.tools.append(pendant)


db.session.commit()

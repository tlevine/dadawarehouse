import sqlalchemy as s

from doeund import Fact, Column

class PiwikEmailOverlap(Fact):
    visitor_id = Column(s.String, primary_key = True)
    email_address = Column(s.String, primary_key = True)
    intersecting_dates = Column(s.Integer)
    unioned_dates = Column(s.Integer)

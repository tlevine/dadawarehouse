import sqlalchemy as s

from doeund import Fact, Column

class EmailAddressDays(Fact):
    'This should just be a view.'
    date = Column(s.Date, primary_key = True)
    email_address = Column(s.String, primary_key = True)

class PiwikVisitorDays(Fact):
    'This should just be a view.'
    date = Column(s.Date, primary_key = True)
    visitor_id = Column(s.String, primary_key = True)

class PiwikEmailOverlap(Fact):
    visitor_id = Column(s.String, primary_key = True)
    email_address = Column(s.String, primary_key = True)
    intersecting_dates = Column(s.Integer)
    unioned_dates = Column(s.Integer)

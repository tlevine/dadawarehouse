import datetime

import sqlalchemy as s
import nose.tools as n

from doeund import database, Fact, Dimension, Column 

class Date(Dimension):
    pk = Column(s.Date, primary_key = True)

class Event(Fact):
    pk = Column(s.Integer, primary_key = True)
    date_id = Column(s.Date, s.ForeignKey(Date.pk))
    date = s.orm.relationship(Date)

def test_create_related():
    engine = s.create_engine('sqlite://')
    session = database(engine)
    date_id = datetime.date(2014,3,2)
    session.add_all(Event(date_id = date_id) for _ in range(4))
    Event.create_related(session)
    session.commit()

    n.assert_equal(session.query(Date).count(), 1)
    n.assert_equal(session.query(Event).count(), 4)

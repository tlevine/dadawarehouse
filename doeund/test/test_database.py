import datetime

import sqlalchemy as s
import nose.tools as n

from doeund import database, Fact, Dimension, Column 

class Hierarchy1(Dimension):
    pk = Column(s.Date, primary_key = True)

class Hierarchy2(Dimension):
    pk = Column(s.Date, primary_key = True)

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Hierarchy1.pk),
                s.ForeignKey(Hierarchy2.pk), primary_key = True)
    hierarchy1 = s.orm.relationship(Hierarchy1)
    hierarchy2 = s.orm.relationship(Hierarchy2)

class Event(Fact):
    pk = Column(s.Integer, primary_key = True)
    date_id = Column(s.Date, s.ForeignKey(Date.pk))
    date = s.orm.relationship(Date)

def test_one_create_related():
    engine = s.create_engine('sqlite://')
    session = database(engine)
    date_id = datetime.date(2014,7,4)
   #session.add_all([Event(date_id = date_id)] * 4)
    session.add_all(Event(date_id = date_id) for _ in range(4))
    session.commit()
    Event.create_related(session)
    session.commit()

    n.assert_equal(session.query(Hierarchy1).count(), 1)
    n.assert_equal(session.query(Hierarchy2).count(), 1)
    n.assert_equal(session.query(Date).count(), 1)
    n.assert_equal(session.query(Event).count(), 4)

def test_multiple_create_related():
    engine = s.create_engine('sqlite://')
    session = database(engine)
    date_id_1 = datetime.date(2014,3,2)
    date_id_2 = datetime.date(2014,8,5)
    session.add_all(Event(date_id = date_id_1) for _ in range(4))
    session.add_all(Event(date_id = date_id_2) for _ in range(4))
    Event.create_related(session)
    session.commit()

    n.assert_equal(session.query(Hierarchy1).count(), 2)
    n.assert_equal(session.query(Hierarchy2).count(), 2)
    n.assert_equal(session.query(Date).count(), 2)
    n.assert_equal(session.query(Event).count(), 8)

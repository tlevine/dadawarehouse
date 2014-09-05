import datetime

import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension

from .base import Column, LabelColumn, PkColumn, FkColumn
from .util import d

class Day(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True)
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    month = Column(s.Integer, default = d(lambda pk: pk.month))
    day = Column(s.Integer, default = d(lambda pk: pk.day))

WEEKDAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
]
class DayOfWeek(Dimension):
    pk = PkColumn()
    dayofweek = Column(s.String, default = d(lambda pk: WEEKDAYS[pk]))

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Day.pk), primary_key = True)
    day = relationship(Day)
    dayofweek_id = FkColumn(DayOfWeek.pk, default = d(lambda pk: pk.weekday()))
    dayofweek = relationship(DayOfWeek)

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

def create_date(session, date_object):
    dayofweek = session.merge(DayOfWeek(pk = date_object.weekday()))
    day = session.merge(Day(pk = date_object))
    date = Date(pk = date_object, dayofweek_id = date_object.weekday())
    return session.merge(date)

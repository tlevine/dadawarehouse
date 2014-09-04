import datetime

import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

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
    dayofweek_id = FkColumn(DayOfWeek.pk, default = d(lambda pk: pk.weekday()))

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

def create_dates(from_date = datetime.date(2010,1,1),
                 to_date = datetime.date.today()):
    for i in range(len(WEEKDAYS)):
        yield DayOfWeek(pk = i)

    one = datetime.timedelta(days = 1)
    today = from_date - one
    while today <= to_date:
        today += one
        yield Day(pk = today)
        yield Date(pk = today)

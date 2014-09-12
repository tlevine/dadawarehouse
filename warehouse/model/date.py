import datetime

import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension

from .base import Column, LabelColumn, PkColumn, FkColumn
from .util import d

WEEKDAYS = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
]

class WeekDay(Dimension):
    pk = PkColumn()
    weekday = LabelColumn(label = 'Day of the week')

class Monthly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    month = Column(s.Integer, default = d(lambda pk: pk.month))
    day = Column(s.Integer, default = d(lambda pk: pk.day))

class Weekly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    week = Column(s.Integer, default = d(lambda pk: pk.isocalendar()[1]))
    weekday_id = FkColumn(WeekDay.pk, default = d(lambda pk: pk.weekday()))
    weekday = relationship(WeekDay)

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Monthly.pk), s.ForeignKey(Weekly.pk),
                primary_key = True)
    day_monthly = relationship(Monthly)
    day_weekly = relationship(Weekly)
    weekday_id = FkColumn(WeekDay.pk, default = d(lambda pk: pk.weekday()))
    weekday = relationship(WeekDay)

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

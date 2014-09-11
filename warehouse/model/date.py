import datetime

import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension

from .base import Column, LabelColumn, PkColumn, FkColumn

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

    @classmethod
    def new(Class, pk):
        return Class(pk = pk, weekday = WEEKDAYS[pk])

class Monthly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer)
    month = Column(s.Integer)
    day = Column(s.Integer)

    @classmethod
    def new(Class, pk):
        return Class(pk = pk, year = pk.year, month = pk.month, day = pk.day)

class Weekly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer)
    week = Column(s.Integer)
    weekday_id = FkColumn(WeekDay.pk)
    weekday = relationship(WeekDay)

    @classmethod
    def new(Class, pk):
        return Class(pk = pk, year = pk.year,
                     week = pk.isocalendar()[1],
                     weekday = WeekDay.new(pk.weekday()))

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Monthly.pk), s.ForeignKey(Weekly.pk),
                primary_key = True)
    day_monthly = relationship(Monthly)
    day_weekly = relationship(Weekly)
    weekday_id = FkColumn(WeekDay.pk)
    weekday = relationship(WeekDay)

    @classmethod
    def new(Class, pk):
        return Class(pk = pk,
                     day_monthly = Monthly(pk = pk),
                     day_weekly = Weekly(pk = pk),
                     weekday = WeekDay(pk = pk.weekday()))

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

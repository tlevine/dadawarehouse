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
    weekday = LabelColumn(label = 'Day of the week',
        default = d(lambda pk: WEEKDAYS[pk.weekday()]))

    @classmethod
    def new(Class, pk):
        return Class(pk = pk)

    def merge(self, session):
        return self._merge_label(self, session, 'weekday')

class Monthly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    month = Column(s.Integer, default = d(lambda pk: pk.month))
    day = Column(s.Integer, default = d(lambda pk: pk.day))

    @classmethod
    def new(Class, pk):
        return Class(pk = pk)

    def merge(self, session):
        return self._merge_pk(session)

class Weekly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    week = Column(s.Integer, default = d(lambda pk: pk.isocalendar()[1]))
    weekday_id = FkColumn(WeekDay.pk, default = d(lambda pk: pk.weekday()))
    weekday = relationship(WeekDay)

    @classmethod
    def new(Class, pk):
        weekly = Class(pk = pk)
        weekly.weekday = WeekDay(pk = weekly.weekday_id)
        return weekly

    def merge(self, session):
        self.weekday = self.weekday.merge(session)
        self._merge_references(session, 'year', 'week', 'weekday')
        return self._merge_pk(session)

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Monthly.pk), s.ForeignKey(Weekly.pk),
                primary_key = True)
    day_monthly = relationship(Monthly)
    day_weekly = relationship(Weekly)
    weekday_id = FkColumn(WeekDay.pk)
    weekday = relationship(WeekDay)

    @classmethod
    def new(Class, pk):
        date = Class(pk = pk)
        date.day_monthly = Monthly.new(pk).merge(session)
        date.day_weekly = Weekly.new(pk).merge(session)
        return date

    def merge(self, session):
        self.day_monthly = self.day_monthly.merge(session)
        self.day_weekly = self.day_weekly.merge(session)
        return self.merge(session)

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

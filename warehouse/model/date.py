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

    def merge(self, session):
        return self.merge_on(self, session, ['weekday'])

class Monthly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    month = Column(s.Integer, default = d(lambda pk: pk.month))
    day = Column(s.Integer, default = d(lambda pk: pk.day))

    def merge(self, session):
        return session.merge(self)

class Weekly(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True, label = 'Day')
    year = Column(s.Integer, default = d(lambda pk: pk.year))
    week = Column(s.Integer, default = d(lambda pk: pk.isocalendar()[1]))
    weekday_id = FkColumn(WeekDay.pk)
    weekday = relationship(WeekDay)

    def merge(self, session):
        self._merge_references(session, references)
        self.weekday = self.weekday.merge(session)
        return session.merge(self)

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Monthly.pk), s.ForeignKey(Weekly.pk),
                primary_key = True)
    day_monthly = relationship(Monthly)
    day_weekly = relationship(Weekly)
    weekday_id = FkColumn(WeekDay.pk)
    weekday = relationship(WeekDay)

    def merge(self, session):
        self.day_monthly = session.merge(Monthly(pk = self.pk))
        self.day_weekly = session.merge(Weekly(pk = self.pk))
        return session.merge(self)

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

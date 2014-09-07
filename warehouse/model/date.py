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
WeekDay = lambda: Column(s.Enum(*WEEKDAYS, name = 'weekday'),
                 label = 'Day of the week',
                 default = d(lambda pk: WEEKDAYS[pk.weekday()]))

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
    weekday = WeekDay()

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(Monthly.pk), s.ForeignKey(Weekly.pk),
                primary_key = True)
    day_monthly = relationship(Monthly)
    day_weekly = relationship(Weekly)
    weekday = WeekDay()
 
    def link(self, session):
        self.day_monthly = Monthly(pk = self.pk)._merge(session)
        self.day_weekly = Weekly(pk = self.pk)._merge(session)
        return session.merge(self)

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

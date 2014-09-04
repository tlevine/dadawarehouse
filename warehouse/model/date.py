import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column, LabelColumn, PkColumn, FkColumn
from .util import d

class PlainDate(Dimension):
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
    dayofweek = LabelColumn(default = d(lambda pk: WEEKDAYS[pk]))

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(PlainDate.pk), primary_key = True,
                onupdate = 'CASCADE')
    dayofweek_id = FkColumn(DayOfWeek.pk, default = d(lambda pk: pk.weekday()))

def DateColumn(*args, **kwargs):
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

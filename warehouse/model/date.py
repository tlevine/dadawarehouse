import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column, LabelColumn

class PlainDate(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True)
    year = Column(s.Integer)
    month = Column(s.Integer)
    day = Column(s.Integer)

class DayOfWeek(Dimension):
    pk = PkColumn()
    dayofweek = LabelColumn()

class Date(Dimension):
    pk = Column(s.Date, s.ForeignKey(PlainDate.pk), primary_key = True)
    dayofweek_id = FkColumn(DayOfWeek.pk)

def DateColumn(*args, **kwargs):
    'A date column with magic hierarchies'
    return Column(s.Date, s.ForeignKey(Date.pk), *args, **kwargs)

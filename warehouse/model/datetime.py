import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column
from .date import Date
from .util import d

def DateTimeColumn(*args, **kwargs):
    return Column(s.Datetime, s.ForeignKey(DateTime.pk), *args, **kwargs)
            
class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = Column(s.Date, default = d(lambda pk: pk.date()))
    time_id = Column(s.Time, default = d(lambda pk: pk.time()))
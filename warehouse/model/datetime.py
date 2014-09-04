import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column
from .date import DateColumn, create_date
from .time import TimeColumn, create_time
from .util import d

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = DateColumn(default = d(lambda pk: pk.date()))
    time_id = TimeColumn(default = d(lambda pk: pk.time()))

def DateTimeColumn(*args, **kwargs):
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **kwargs)

def create_datetime(datetime):
    return create_date(datetime.date()) + create_time(datetime.time())

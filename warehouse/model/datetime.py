import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column
from .date import DateColumn
from .time import TimeColumn
from .util import d

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = DateColumn(default = d(lambda pk: pk.date()))
    time_id = TimeColumn(default = d(lambda pk: pk.time()))

def DateTimeColumn(*args, **kwargs):
    _kwargs = dict(kwargs)
    if 'onupdate' not in _kargs:
        _kwargs['onupdate'] = 'CASCADE'
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **_kwargs)

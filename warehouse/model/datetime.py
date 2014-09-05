import sqlalchemy as s

from doeund import Dimension

from .base import Column
from .util import d

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date = Column(s.Date, default = d(lambda pk: pk.date()))
    time = Column(s.Time, default = d(lambda pk: pk.time()))

def DateTimeColumn(*args, **kwargs):
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **kwargs)

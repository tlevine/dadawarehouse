import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension

from .base import Column
from .date import Date
from .time import Time
from .util import d

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = Column(s.Date, s.ForeignKey(Date.pk),
                     default = d(lambda pk: pk.date()))
    date = relationship(Date)

    time_id = Column(s.Time, s.ForeignKey(Time.pk),
                     default = d(lambda pk: pk.time()))
    time = relationship(Time)

def DateTimeColumn(*args, **kwargs):
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **kwargs)

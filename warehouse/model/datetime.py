import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension

from .base import Column
from .date import Date
from .time import Time

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = Column(s.Date, s.ForeignKey(Date.pk))
    date = relationship(Date)

    time_id = Column(s.Time, s.ForeignKey(Time.pk))
    time = relationship(Time)

    @classmethod
    def new(Class, pk):
        return Class(pk = pk, date = Date.new(pk.date()),
                     time = Time.new(pk.time()))

def DateTimeColumn(*args, **kwargs):
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **kwargs)

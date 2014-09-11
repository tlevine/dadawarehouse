import datetime

import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column

class Time(Dimension):
    pk = Column(s.Time, primary_key = True)
    hour = Column(s.Integer)
    minute = Column(s.Integer, default = d(lambda pk: pk.minute))

    @classmethod
    def new(Class, pk):
        return Class(pk = pk, hour = pk.hour, minute = pk.minute)

def TimeColumn(*args, **kwargs):
    return Column(s.Time, s.ForeignKey(Time.pk), *args, **kwargs)

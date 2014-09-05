import datetime

import sqlalchemy as s

from doeund import Fact as _Fact, Dimension

from .base import Column
from .util import d

class Time(Dimension):
    pk = Column(s.Time, primary_key = True)
    hour = Column(s.Integer, default = d(lambda pk: pk.hour))
    minute = Column(s.Integer, default = d(lambda pk: pk.minute))

def TimeColumn(*args, **kwargs):
    return Column(s.Time, s.ForeignKey(Time.pk), *args, **kwargs)

def create_time(session, time_object):
    return session.merge(Time(pk = time_object))

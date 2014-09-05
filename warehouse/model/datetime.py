import sqlalchemy as s

from doeund import Dimension

from .base import Column
from .date import Date, create_date
from .time import Time, create_time
from .util import d

class DateTime(Dimension):
    pk = Column(s.DateTime, primary_key = True)
    date_id = Column(s.Date, s.ForeignKey(Date.pk), default = d(lambda pk: pk.date()))
    time_id = Column(s.Time, s.ForeignKey(Time.pk), default = d(lambda pk: pk.time()))

def DateTimeColumn(*args, **kwargs):
    return Column(s.DateTime, s.ForeignKey(DateTime.pk), *args, **kwargs)

def create_datetime(session, datetime_object):
    date = create_date(session, datetime_object.date())
    time = create_time(session, datetime_object.time())
    datetime = DateTime(pk = datetime_object, date_id = date.pk, time_id = time.pk)
    return session.merge(datetime)

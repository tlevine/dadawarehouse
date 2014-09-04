import datetime

from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from .date import create_date
from .time import create_time
from .datetime import DateTime

def create_datetime(d):
    return create_date(d.date()) + create_time(d.time()) + \
           [DateTime(date_id = d.date(), time_id = d.time())]

TEMPORALS = {
    datetime.date: create_date,
    datetime.time: create_time,
    datetime.datetime: create_datetime,
}
def create_temporal(session, temporal):
    for record in TEMPORALS[type(temporal)](temporal):
        session.add(record)
        try:
            session.commit()
        except IntegrityError:
            if type(record) == datetime.datetime:
                print(record)
            session.rollback()
        except:
            raise
        else:
            pass

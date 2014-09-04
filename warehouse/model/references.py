import datetime

from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from .date import create_date
from .time import create_time
from .datetime import create_datetime

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
            session.rollback()
        except FlushError:
            session.rollback()
        except:
            raise

import datetime

from sqlalchemy.orm.exc import NoResultFound

from .date import Date
from .time import Time
from .datetime import Datetime

MAPPING = {
    datetime.time: Time,
    datetime.date: Date,
    datetime.datetime: DateTime,
}

def upsert_temporal(session, temporal):
    '''
    session :: A SQLAlchemy session
    temporal :: a date, time, or datetime, which functions as a primary key
                on the corresponding table
    '''
    Dimension = MAPPING[type(temporal)]
    try:
        record = session.query(Dimension).filter(Dimension.pk = temporal).one()
    except NoResultFound:
        record = Dimension(pk = temporal)
        session.add(record)
    return record

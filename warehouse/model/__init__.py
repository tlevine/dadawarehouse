import datetime

from doeund import Fact, Dimension

from .base import Column, PkColumn, FkColumn, LabelColumn
from .date import Date, DateColumn, DayOfWeek, create_dates
from .time import Time, TimeColumn, create_times

def create_datetimes(from_date = datetime.date(2010, 1, 1),
                     to_date = datetime.date.today()):
    yield from create_dates(from_date = from_date, to_date = to_date)
    yield from create_times()

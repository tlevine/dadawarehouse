import os

import sqlalchemy as s

from .model import Fact, Dimension, Column, IdColumn, Date
from sqlalchemy import ForeignKey, String

class CalendarFilename(Dimension):
    pk = IdColumn(primary_key = True)
    filename = Column(String, unique = True)

class CalendarDescription(Dimension):
    pk = IdColumn(primary_key = True)
    description = Column(String, unique = True)

class CalendarFile(Dimension):
    code = Column(s.String(2), primary_key = True)
    filename_id = IdColumn(ForeignKey(CalendarFilename.pk))
    description_id = IdColumn(ForeignKey(CalendarDescription.pk))

class CalendarEvent(Fact):
    pk = Column(s.Integer, primary_key = True)
    calendar = Column(s.String(2), s.ForeignKey(CalendarFile.code))
    date = Column(s.Date, s.ForeignKey(Date.pk))
    description = IdColumn(s.ForeignKey(CalendarDescription))

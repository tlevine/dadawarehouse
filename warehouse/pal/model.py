import os

import sqlalchemy as s

from ..model import Fact, Dimension, Column, PkColumn, FkColumn, LabelColumn, Date, Time
from sqlalchemy import ForeignKey, String

class CalendarFilename(Dimension):
    pk = PkColumn()
    filename = LabelColumn()

class CalendarDescription(Dimension):
    pk = PkColumn()
    description = LabelColumn()

class CalendarFile(Dimension):
    code = Column(s.String(2), primary_key = True)
    filename_id = FkColumn(CalendarFilename.pk)
    description_id = FkColumn(CalendarDescription.pk)

class CalendarEvent(Fact):
    pk = PkColumn()
    calendar = Column(s.String(2), s.ForeignKey(CalendarFile.code))
    date = Column(s.Date, s.ForeignKey(Date.pk))
    description = FkColumn(CalendarDescription))

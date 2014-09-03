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
    pk = Column(s.String(2), primary_key = True)
    filename = FkColumn(CalendarFilename.pk)
    description = FkColumn(CalendarDescription.pk)

class CalendarEventDescription(Dimension):
    pk = PkColumn()
    eventdescription = LabelColumn()

class CalendarEvent(Fact):
    pk = PkColumn()
    calendar = Column(s.String(2), s.ForeignKey(CalendarFile.code))
    date = DateColumn()
    description = FkColumn(CalendarEventDescription.pk)

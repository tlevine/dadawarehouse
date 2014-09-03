import os

import sqlalchemy as s

import ..model as m
from sqlalchemy import ForeignKey, String

class CalendarFilename(m.Dimension):
    pk = m.PkColumn()
    filename = m.LabelColumn()

class CalendarDescription(m.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

class CalendarFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.FkColumn(CalendarFilename.pk)
    description = m.FkColumn(CalendarDescription.pk)

class CalendarEventDescription(m.Dimension):
    pk = m.PkColumn()
    eventdescription = m.LabelColumn()

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    calendar = m.Column(String(2), ForeignKey(CalendarFile.code))
    date = m.DateColumn()
    description = m.FkColumn(CalendarEventDescription.pk)

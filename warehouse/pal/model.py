import os

import sqlalchemy as s

import warehouse.model as m
from sqlalchemy import ForeignKey, String

class CalendarFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.Column(String, unique = True)
    description = m.Column(String)

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    calendar = m.Column(String(2), ForeignKey(CalendarFile.pk))
    date = m.DateColumn()
    description = m.Column(String)

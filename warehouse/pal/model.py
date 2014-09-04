import os

import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import warehouse.model as m

class CalendarFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.Column(String, unique = True)
    description = m.Column(String)
    events = relationship('CalendarEvent', backref = 'file')

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(CalendarFile.pk))
    date = m.Column(Date)
    description = m.Column(String)

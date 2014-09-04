import os

import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String

import warehouse.model as m

class CalendarFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.Column(String, unique = True)
    description = m.Column(String)
    events = relationship('CalendarEvent', backref = 'file')

class CalendarEventDescription(m.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(CalendarFile.pk))
    date_id = m.DateColumn()
    description_id = m.FkColumn(CalendarEventDescription.pk)
    description = relationship(CalendarEventDescription)

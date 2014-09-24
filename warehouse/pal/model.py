import os

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import warehouse.model as m

class File(m.Dimension):
    pk = m.Column(String(2), primary_key = True, label = 'Two-letter code')
    filename = m.Column(String, unique = True, label = 'File name')
    description = m.Column(String)

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(File.pk))
    file = relationship(File)
    date = m.Column(Date)
    description = m.Column(String)

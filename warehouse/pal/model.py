import os

import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import doeund as d

import warehouse.model as m

class File(d.Dimension):
    pk = m.Column(String(2), primary_key = True, label = 'Two-letter code')
    filename = m.Column(String, unique = True, label = 'File name')
    description = m.Column(String)

class Description(d.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

    @classmethod
    def new(Class, description):
        return Class(description = description)

class CalendarEvent(d.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(File.pk))
    file = relationship(File)
    date_id = m.DateColumn()
    date = relationship(m.Date)
    description_id = m.FkColumn(Description.pk)
    description = relationship(Description)

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

    def link(self, session):
        return session.merge(self)

class Description(d.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

    def link(self, session):
        return d.merge_on_unique(self.__class__, session,
            Description.description, self.description)

class CalendarEvent(d.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(File.pk))
    file = relationship(File)
    date_id = m.DateColumn()
    date = relationship(m.Date)
    description_id = m.FkColumn(Description.pk)
    description = relationship(Description)
    
    def link(self, session):
        '''
        Link to dependencies.
        '''
        event_date = m.Date(pk = self.date).link(session)
        event_description = Description(
            description = self.description).link(session)
        self.date = event_date
        self.description = event_description
        return self # Don't need to merge because duplicates are allowed

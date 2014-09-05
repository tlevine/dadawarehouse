import os

import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import doeund as d

import warehouse.model as m

class CalendarFile(d.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.Column(String, unique = True)
    description = m.Column(String)

    def merge(self, session):
        return session.merge(self)

class CalendarEventDescription(d.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

    def merge(self, session):
        return d.merge_on_unique(self.__class__, session,
            CalendarEventDescription.description, self.description)

class CalendarEvent(d.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(CalendarFile.pk))
    file = relationship(CalendarFile)
    date_id = m.DateColumn()
    date = relationship(m.Date)
    description_id = m.FkColumn(CalendarEventDescription.pk)
    description = relationship(CalendarEventDescription)
    
    def link(self, session):
        '''
        Link to dependencies.
        '''
        event_date = m.create_date(session, self.date)
        event_description = CalendarEventDescription(
            description = self.description).merge(session)
        self.date = event_date
        self.description = event_description
        return self

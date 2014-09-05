import os

import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import warehouse.model as m

class CalendarFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True)
    filename = m.Column(String, unique = True)
    description = m.Column(String)

    @classmethod
    def get(Class, session, code, filename, description):
        return session.merge(Class(pk = code, filename = filename,
                                   description = description))

class CalendarEventDescription(m.Dimension):
    pk = m.PkColumn()
    description = m.LabelColumn()

    @classmethod
    def get(Class, session, description):
        x = session.query(Class).filter(Class.description == description).first()
        if x == None:
            x = Class(description = description)
            session.add(x)
        return x

class CalendarEvent(m.Fact):
    pk = m.PkColumn()
    file_id = m.Column(String(2), ForeignKey(CalendarFile.pk))
    file = relationship(CalendarFile)
    date_id = m.DateColumn()
    date = relationship(m.Date)
    description_id = m.FkColumn(CalendarEventDescription.pk)
    description = relationship(CalendarEventDescription)
    
    @classmethod
    def new(Class, session, calendar_file, event_date, event_description):
        '''
        calendar_file is an SQLAlchemy record object thingy.
        '''
        event_date = m.create_date(session, event_date)
        event_description = CalendarEventDescription.get(session, event_description)
        return Class(file = calendar_file, date = event_date, description = event_description)

import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class Message(d.Dimension):
    pk = d.Column(s.String, primary_key = True)
    date_id = m.DateColumn()
    thread_id = d.Column(s.String, s.ForeignKey(Thread))

class NotmuchMessage(d.Fact):
    pk = m.PkColumn()

    # Could be unique identifiers
    message_id = d.Column(s.String, s.ForeignKey(Message.pk))
    filename = d.Column(s.String)

    # Foreign Keys
    date_id = m.DateColumn()
    thread_id = d.Column(s.String, s.ForeignKey(Thread))

class NotmuchMessagePart(d.Fact):
    message_id = d.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    part = d.Column(s.Integer, primary_key = True)
    name = d.Column(s.String)

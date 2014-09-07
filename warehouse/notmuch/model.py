import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class Person(d.Dimension):
    pk = PkColumn()
    name = d.Column(s.String)

class Address(d.Dimension):
    pk = d.Column(s.String, primary_key = True)
    person_id = d.FkColumn(Person.pk)

class Message(d.Dimension):
    pk = d.Column(s.String, primary_key = True)
    datetime_id = m.DateTimeColumn()
    thread_id = d.Column(s.String, s.ForeignKey(Thread))
    filename = d.Column(s.String)
    subject = d.Column(s.String)
    from_address = d.FkColumn(Address.pk)

class NotmuchCorrespondance(d.Fact):
    '''
    to_address includes CC, BCC
    '''
    pk = d.PkColumn()
    from_address = d.Column(s.String, s.ForeignKey(Address.pk))
    to_address = d.Column(s.String, s.ForeignKey(Address.pk))

class NotmuchMessage(d.Fact):
    pk = d.Column(s.String, primary_key = True)

class NotmuchMessagePart(d.Fact):
    message_id = d.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    part = d.Column(s.Integer, primary_key = True)
    name = d.Column(s.String)

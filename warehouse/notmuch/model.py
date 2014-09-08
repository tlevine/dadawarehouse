import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class Address(d.Dimension):
    pk = m.Column(s.String, primary_key = True)
    name = m.Column(s.String)

class Thread(d.Dimension):
    pk = m.Column(s.String, primary_key = True)

class Message(d.Dimension):
    pk = m.Column(s.String, primary_key = True)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    thread_id = m.Column(s.String, s.ForeignKey(Thread.pk))
    thread = relationship(Thread)
    filename = m.Column(s.String)
    subject = m.Column(s.String)
    from_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    from_address = relationship(Address)
    def link(self, session):
        self.datetime = self.datetime.link(session)
        self.from_address = session.merge(self.from_address)
        self.thread = session.merge(self.thread)
        return self

class NotmuchCorrespondance(d.Fact):
    '''
    to_address includes CC, BCC
    '''
    pk = m.PkColumn()
    from_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    from_address = relationship(Address, foreign_keys = [from_address_id])
    to_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    to_address = relationship(Address, foreign_keys = [to_address_id])
    def link(self, session):
        self.from_address = self.from_address.link(session)
        self.to_address = self.to_address.link(session)
        return self

class NotmuchMessage(d.Fact):
    pk = m.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    message = relationship(Message)
    def link(self, session):
        self.message = self.message.link(session)
        return self

class ContentType(d.Dimension):
    pk = m.PkColumn()
    content_type = m.LabelColumn()

class NotmuchAttachment(d.Fact):
    message_id = m.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    message = relationship(Message)
    part_number = m.Column(s.Integer, primary_key = True)
    content_type_id = m.FkColumn(ContentType.pk, nullable = True)
    content_type = relationship(ContentType)
    name = m.Column(s.String)
    def link(self, session):
       #self.message = self.message.link(session)
        if self.content_type != None:
            self.content_type = d.merge_on_unique(ContentType, session,
                ContentType.content_type, self.content_type)
        return self

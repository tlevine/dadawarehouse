import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class Address(d.Dimension):
    pk = m.Column(s.String, primary_key = True)
    name = m.Column(s.String)
    def link(self, session):
        return session.merge(self)

class Thread(d.Dimension):
    pk = m.Column(s.String, primary_key = True)
    def link(self, session):
        return session.merge(self)

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
        self.from_address = self.from_address.link(session)
        return session.merge(self)

class NotmuchCorrespondance(d.Fact):
    '''
    to_address includes CC, BCC
    '''
    pk = m.PkColumn()
    from_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    from_address = relationship(Address)
    to_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    from_address = relationship(Address)
    def link(self, session):
        self.from_address = self.from_address.link(session)
        self.to_address = self.to_address.link(session)
        return self

class NotmuchMessage(d.Fact):
    pk = m.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    message = relationship(Message)
    def link(self, session):
        self.message = self.message.link(session)
        return session.merge(self)

class ContentType(d.Dimension):
    pk = m.PkColumn()
    content_type = m.LabelColumn()
    def link(self, session):
        return d.merge_on_unique(ContentType, session,
                                 ContentType.content_type,
                                 self.content_type)

class NotmuchAttachment(d.Fact):
    message_id = m.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    message = relationship(Message)
    content_type_id = m.FkColumn(ContentType.pk)
    content_type = relationship(ContentType)
    part_number = m.Column(s.Integer, primary_key = True)
    name = m.Column(s.String)
    def link(self, session):
        self.message = self.message.link(session)
        self.content_type = self.content_type.link(session)
        return session.merge(self)

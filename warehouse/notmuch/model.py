import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class Address(d.Dimension):
    pk = m.PkColumn()
    address = m.LabelColumn()

class Name(d.Dimension):
    pk = m.PkColumn()
    name = m.LabelColumn()

class ContentType(d.Dimension):
    pk = m.PkColumn()
    content_type = m.LabelColumn()

class Message(d.Dimension):
    pk = m.PkColumn()
    notmuch_message_id = m.Column(s.String)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    thread_id = m.Column(s.String)
    filename = m.Column(s.String)
    subject = m.Column(s.String)
    from_address_id = m.FkColumn(Address.pk)
    from_address = relationship(Address)

class AddressName(d.Fact):
    __table_args__ = (s.UniqueConstraint('address_id', 'name_id'),)
    pk = m.PkColumn()
    address_id = m.FkColumn(Address.pk, unique = True)
    address = relationship(Address)
    name_id = m.FkColumn(Name.pk, unique = True)
    name = relationship(Name)

class NotmuchCorrespondance(d.Fact):
    '''
    to_address includes CC, BCC
    '''
    pk = m.PkColumn()
    from_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    from_address = relationship(Address, foreign_keys = [from_address_id])
    to_address_id = m.Column(s.String, s.ForeignKey(Address.pk))
    to_address = relationship(Address, foreign_keys = [to_address_id])

class NotmuchMessage(d.Fact):
    pk = m.Column(s.String, s.ForeignKey(Message.pk), primary_key = True)
    message = relationship(Message)

class NotmuchAttachment(d.Fact):
    message_id = m.FkColumn(Message.pk, primary_key = True)
    message = relationship(Message)
    part_number = m.Column(s.Integer, primary_key = True)
    content_type_id = m.FkColumn(ContentType.pk, nullable = True)
    content_type = relationship(ContentType)
    name = m.Column(s.String)

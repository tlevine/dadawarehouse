import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class EmailMessage(m.Dimension):
    pk = m.PkColumn()
    notmuch_message_id = m.Column(s.String)
    datetime = m.Column(s.DateTime)
    thread_id = m.Column(s.String)
    filename = m.Column(s.String)
    subject = m.Column(s.String)
    from_address = m.Column(s.String)

class EmailAddressName(m.Fact):
    __table_args__ = (s.UniqueConstraint('address', 'name'),)
    pk = m.PkColumn()
    address = m.Column(s.String)
    name = m.Column(s.String)

class EmailCorrespondance(m.Fact):
    '''
    to_address includes CC, BCC
    '''
    pk = m.PkColumn()
    message_id = m.FkColumn(Message.pk)
    from_address = m.Column(s.String)
    to_address = m.Column(s.String))

class EmailAttachment(m.Fact):
    message_id = m.FkColumn(Message.pk, primary_key = True)
    message = relationship(Message)
    part_number = m.Column(s.Integer, primary_key = True)
    content_type = m.Column(s.String)
    name = m.Column(s.String)

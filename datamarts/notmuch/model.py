import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class EmailMessage(m.Fact):
    message_id = m.Column(s.String, primary_key = True)
    datetime = m.Column(s.DateTime)
    thread_id = m.Column(s.String)
    filename = m.Column(s.String)
    subject = m.Column(s.String)
    from_name = m.Column(s.String, nullable = True)
    from_address = m.Column(s.String)

class EmailRecipients(m.Helper):
    '''
    to_address includes CC, BCC
    '''
    pk = m.PkColumn()
    message_id = m.Column(s.String, s.ForeignKey(EmailMessage.message_id))
    message = relationship(EmailMessage)
    to_name = m.Column(s.String)
    to_address = m.Column(s.String)

class EmailAttachment(m.Fact):
    message_id = m.Column(s.String,
                          s.ForeignKey(EmailMessage.message_id),
                          primary_key = True)
    message = relationship(EmailMessage)
    part_number = m.Column(s.Integer, primary_key = True)
    content_type = m.Column(s.String, nullable = True)
    name = m.Column(s.String, nullable = True)

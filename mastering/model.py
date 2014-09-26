'''
Mappings between service-specific identifiers ("local_id")
and global identifiers ("global_id") for different services

The global identifier is in the format that I use in
my mutt alias file, which is approximately one of these.

* ``[first name].[last name]``
* ``[first name].[middle name].[last name]``
* ``[first name].[last name].[context, like a city]``

I use the last of these if the others would be ambiguous
because different people have the same name.
'''

import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgres import CIDR

from doeund.base import Base, Dimension, Column
from datamarts import (
    BranchableLog,
    FacebookMessage, FacebookChatStatusChange,
    FacebookDuration, FacebookNameChange,


class ProtoMaster(Base):
    '''
    A place to store the guesses of what the master data might be
    '''
    __tablename__ = 'proto_master'
    pk = PkColumn()
    context = Column(s.String)
    global_id = Column(s.String)
    local_id = Column(s.String)

GidColumn = Column(s.String, nullable = True)

class Facebook(Dimension):
    global_id = GidColumn
    local_id = Column(s.BigInteger, primary_key = True)
    messages = relationship(FacebookMessage,
        primaryjoin = 'FacebookMessage.user_id == Facebook.local_id')
    chat_status_changes = relationship(FacebookChatStatusChange,
        primaryjoin = 'FacebookChatStatusChange.user_id == Facebook.local_id')
    durations = relationship(FacebookDuration,
        primaryjoin = 'FacebookDuration.user_id == Facebook.local_id')
    name_changes = relationship(FacebookNameChange,
        primaryjoin = 'FacebookNameChanges.user_id == Facebook.local_id')

class Twitter(Dimension):
    global_id = GidColumn
    local_id = Column(s.String, primary_key = True)

class Name(Dimension):
    pk = PkColumn()
    global_id = GidColumn
    name = Column(s.String)
    emails_from = relationship(EmailMessage,
        primaryjoin = 'EmailAddress.name == EmailMessage.from_name')
   #emails_to = relationship(EmailMessage,
   #    primaryjoin = 'EmailAddress.email_address == EmailMessage.to_address')

class IPAddress(Dimension):
    pk = PkColumn()
    global_id = GidColumn
    ip_address = Column(CIDR)
    branchable_logs = relationship(BranchableLog,
        primaryjoin = 'BranchableLog.ip_address == IPAddress.ip_address')

class EmailAddress(Dimension):
    global_id = GidColumn
    email_address = Column(s.String, primary_key = True)
    emails_from = relationship(EmailMessage,
        primaryjoin = 'EmailAddress.email_address == EmailMessage.from_address')
   #emails_to = relationship(EmailMessage,
   #    primaryjoin = 'EmailAddress.email_address == EmailMessage.to_address')

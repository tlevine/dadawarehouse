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
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgres import CIDR

from doeund import Base, Fact, Dimension, Column, PkColumn
from datamarts import (
    BranchableLog,
    FacebookMessage, FacebookChatStatusChange,
    FacebookDuration, FacebookNameChange,
    MuttAlias,
    NotmuchMessage, NotmuchRecipient, NotmuchAttachment,
)

class Person(Dimension):
    pk = Column(s.String, primary_key = True)
    ip_addresses = relationship('IPAddress', lazy = 'dynamic',
        primaryjoin = 'Person.pk == IPAddress.global_id')
    facebooks = relationship('Person', lazy = 'dynamic',
        primaryjoin = 'Person.pk == Facebook.global_id')
    email_addresses = relationship('EmailAddress', lazy = 'dynamic',
        primaryjoin = 'Person.pk == EmailAddress.global_id')
    twitters = relationship('Twitter', lazy = 'dynamic',
        primaryjoin = 'Person.pk == Twitter.global_id')

GidColumn = lambda: Column(s.String, s.ForeignKey(Person.pk), nullable = True)

class Facebook(Dimension):
    global_id = GidColumn()
    local_id = Column(s.BigInteger, primary_key = True)
    messages = relationship(FacebookMessage, lazy = 'dynamic',
        primaryjoin = 'FacebookMessage.user_id == Facebook.local_id')
    chat_status_changes = relationship(FacebookChatStatusChange, lazy = 'dynamic',
        primaryjoin = 'FacebookChatStatusChange.user_id == Facebook.local_id')
    durations = relationship(FacebookDuration, lazy = 'dynamic',
        primaryjoin = 'FacebookDuration.user_id == Facebook.local_id')
    name_changes = relationship(FacebookNameChange, lazy = 'dynamic',
        primaryjoin = 'FacebookNameChanges.user_id == Facebook.local_id')

class Twitter(Dimension):
    global_id = GidColumn()
    local_id = Column(s.String, primary_key = True)

class Name(Fact):
    pk = PkColumn()
    global_id = GidColumn()
    name = Column(s.String)

class IPAddress(Dimension):
    pk = PkColumn()
    global_id = GidColumn()
    ip_address = Column(CIDR)
    branchable_logs = relationship(BranchableLog,
        primaryjoin = 'BranchableLog.ip_address == IPAddress.ip_address')

class EmailAddress(Dimension):
    global_id = GidColumn()
    email_address = Column(s.String, primary_key = True)
    emails_from = relationship(NotmuchMessage, lazy = 'dynamic',
        primaryjoin = 'NotmuchAddress.email_address == NotmuchMessage.from_address')
    emails_to = relationship(NotmuchMessage, lazy = 'dynamic',
        primaryjoin = 'NotmuchAddress.email_address == NotmuchMessage.to_address')

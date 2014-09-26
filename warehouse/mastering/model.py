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

from .base import Base, Dimension, Column

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

class Twitter(Dimension):
    global_id = GidColumn
    local_id = Column(s.String, primary_key = True)

class Name(Dimension):
    pk = PkColumn()
    global_id = GidColumn
    name = Column(s.String)

class IPAddress(Dimension):
    pk = PkColumn()
    global_id = GidColumn
    ip_address = Column(CIDR)
    branchable_logs = relationship(IPAddress,
        primaryjoin = 'BranchableLog.ip_address == IPAddress.ip_address')

class EmailAddress(Dimension):
    global_id = GidColumn
    email_address = Column(s.String, primary_key = True)

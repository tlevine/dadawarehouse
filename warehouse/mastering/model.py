import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from ..model import Base, Column

def GidColumn():
    return Column(s.String)

class PersonIdentifier(Base):
    '''
    Map between service-specific identifiers ("local_id")
    and global identifiers ("global_id"), for different
    services ("service").

    The global identifier is in the format that I use in
    my mutt alias file, which is approximately one of these.

    * ``[first name].[last name]``
    * ``[first name].[middle name].[last name]``
    * ``[first name].[last name].[context, like a city]``

    I use the last of these if the others would be ambiguous
    because different people have the same name.
    '''
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'master_' + Class.__name__.lower()

class ProtoMaster(Base):
    '''
    A place to store the guesses of what the master data might be
    '''
    __tablename__ = 'proto_master'
    pk = PkColumn()
    context = Column(s.String)
    global_id = GidColumn()
    local_id = Column(s.BigInteger)

class Facebook(PersonIdentifier):
    pk = PkColumn()
    global_id = GidColumn()
    local_id = Column(s.BigInteger, unique = True)

class Twitter(PersonIdentifier):
    pk = PkColumn()
    global_id = GidColumn()
    local_id = Column(s.String, unique = True)

class Name(PersonIdentifier):
    pk = PkColumn()
    global_id = GidColumn()
    name = Column(s.String)

class EmailAddress(PersonIdentifier):
    pk = PkColumn()
    global_id = GidColumn()
    email_address = Column(s.String, unique = True)

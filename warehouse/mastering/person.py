import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from .base import Base
from .columns import Column

class Person(Base):
    __tablename__ = 'master_person'
    pk = Column(s.String, primary_key = True) # from the mutt alias file
    facebook = Column(s.BigInteger, nullable = True)
    twitter = Column(s.String, nullable = True)
    email_addresses = relationship('EmailAddress')

class EmailAddress(Base):
    __tablename__ = 'master_emailaddress'
    email_address = Column(s.String, primary_key = True)
    person_id = Column(s.String, s.ForeignKey(Person.pk))

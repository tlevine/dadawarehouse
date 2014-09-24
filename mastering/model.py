import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import ..model as m

Base = declarative_base()

class EmailAddress(Base):
    __tablename__ = 'emailaddress'
    email_address = m.Column(s.String, primary_key = True)
    person_id = m.Column(s.String, s.ForeignKey(Person.pk))

class Person(Base):
    __tablename__ = 'person'
    pk = m.Column(s.String, primary_key = True) # from the mutt alias file
    facebook = m.Column(s.BigInteger, nullable = True)
    twitter = m.Column(s.String, nullable = True)
    email_addresses = relationship(EmailAddress)

import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import warehouse.model.base as m

class Person(m.Base):
    __tablename__ = 'master_person'
    pk = m.Column(s.String, primary_key = True) # from the mutt alias file
    facebook = m.Column(s.BigInteger, nullable = True)
    twitter = m.Column(s.String, nullable = True)
    email_addresses = relationship('EmailAddress')

class EmailAddress(m.Base):
    __tablename__ = 'master_emailaddress'
    email_address = m.Column(s.String, primary_key = True)
    person_id = m.Column(s.String, s.ForeignKey(Person.pk))

import sqlalchemy as s
from sqlalchemy.orm import relationship, backref
import ..model as m

class EmailAddress(m.Fact):
    person_id = m.Column(s.String, s.ForeignKey(Person.pk))
    value = m.Column(s.String)

class Person(m.Dimension):
    pk = m.Column(s.String, primary_key = True) # from the mutt alias file
    facebook = m.Column(s.BigInteger, nullable = True)
    twitter = m.Column(s.String, nullable = True)
    email_addresses = relationship(EmailAddress)

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
import os

import sqlalchemy as s
from sqlalchemy.orm import relationship, sessionmaker
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

GidColumn = lambda: Column(s.String, s.ForeignKey(Person.pk), nullable = True)

class Facebook(Dimension):
    global_id = GidColumn()
    local_id = Column(s.BigInteger, primary_key = True)

FacebookMessage.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookChatStatusChange.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookDuration.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookNameChange.add_join('dim_facebook', [('user_id', 'local_id')])

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

BranchableLog.add_join('dim_ipaddress', [('ip_address', 'ip_address')])

class EmailAddress(Dimension):
    global_id = GidColumn()
    email_address = Column(s.String, primary_key = True)

NotmuchMessage.add_join('dim_emailaddress', [('email_address', 'from_address')])
NotmuchMessage.add_join('dim_emailaddress', [('email_address', 'to_address')])

file_mapping = [
    ('person.csv', Person),
    ('facebook.csv', Facebook),
    ('name.csv', Name),
    ('emailaddress.csv', EmailAddress),
    ('ipaddress.csv', IPAddress),
]
def load(directory, engine):
    session = sessionmaker(bind=engine)()
    for filename, Class in file_mapping:
        with open(os.path.join(directory, filename)) as fp:
            reader = csv.DictReader(fp)
            session.add_all(Class(**row) for row in reader)
    session.commit()

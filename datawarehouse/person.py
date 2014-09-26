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
import csv

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
    global_id = Column(s.String, primary_key = True)

GidColumn = lambda: Column(s.String, s.ForeignKey(Person.global_id), nullable = True)

class Facebook(Dimension):
    global_id = GidColumn()
    local_id = Column(s.BigInteger, primary_key = True)

FacebookMessage.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookChatStatusChange.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookDuration.add_join('dim_facebook', [('user_id', 'local_id')])
FacebookNameChange.add_join('dim_facebook', [('user_id', 'local_id')])

class Twitter(Dimension):
    global_id = GidColumn()
    person = relationship(Person)
    local_id = Column(s.String, primary_key = True)

class Name(Fact):
    pk = PkColumn(hide = True)
    global_id = GidColumn()
    person = relationship(Person)
    name = Column(s.String)

class IPAddress(Dimension):
    pk = PkColumn(hide = True)
    global_id = GidColumn()
    person = relationship(Person)
    ip_address = Column(CIDR)

BranchableLog.add_join('dim_ipaddress', [('ip_address', 'ip_address')])

class EmailAddress(Dimension):
    global_id = GidColumn()
    person = relationship(Person)
    email_address = Column(s.String, primary_key = True)

NotmuchMessage.add_join('dim_emailaddress', [('from_address', 'email_address')])
# NotmuchMessage.add_join('dim_emailaddress', [('to_address', 'email_address')])

file_mapping = [
    ('facebook.csv', Facebook),
    ('name.csv', Name),
    ('emailaddress.csv', EmailAddress),
    ('ipaddress.csv', IPAddress),
]

def _strip(dictionary):
    return {k.strip():v.strip() for k,v in dictionary.items()}

def load(directory, engine):
    session = sessionmaker(bind=engine)()
    for filename, Class in file_mapping:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))
                new_global_ids = set(row['global_id'] for row in rows) - \
                                 set(session.query(Person.global_id))
                break
                session.add_all(Person(pk = pk) for pk in new_global_ids)
                session.query(Class).delete()
                session.add_all(Class(**row) for row in rows)
        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())
    session.commit()

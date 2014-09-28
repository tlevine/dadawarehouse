import os
import csv
from collections import defaultdict

from sqlalchemy.ext.declarative import declarative_base

from datamarts import (
    BranchableLog,
    FacebookNameChange,
    MuttAlias,
    NotmuchMessage,
    PiwikVisit,
    TwitterAction,
)

from .model import Person, EmailAddress, Facebook, Twitter

file_mapping = [
    ('emailaddress.csv', Person.email_addresses, EmailAddress),
    ('facebook.csv', Person.facebooks, Facebook),
    ('twitter.csv', Person.twitters, Twitter),
    ('name.csv', Person.names, None),
    ('ipaddress.csv', Person.ip_addresses, None),
    ('piwik.csv', Person.piwiks, None),
]

def _strip(dictionary):
    return {k.strip():v.strip() for k,v in dictionary.items()}

def load_notmuch(session):
    name_addresses = session.query(NotmuchMessage.from_name,
                                   NotmuchMessage.from_address).distinct()
    for name, address in name_addresses:
        person = session.query(Person)\
                        .join(EmailAddress)\
                       #.join(EmailAddress,
                       #      Person.id == EmailAddress.person_id)\
                        .filter(EmailAddress.emailaddress == address)\
                        .first()
        person.email_addresses = set(person.email_addresses).union({address})
        person.names = set(person.names).union({name})
        session.flush()

def load_branchable():
def load_facebook():
def load_muttalias():
def load_piwik():
def load_twitter():

def load_sql(session):
    load_notmuch(session)

def load_csv(session, directory):
    for filename, column, Class in file_mapping:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))

                new_person_ids = set(row['person_id'] for row in rows) - \
                                 set(session.query(Person.id))
                session.add_all(Person(id = pid) for pid in new_person_ids)

                person_sets = defaultdict(lambda: set())
                for row in rows:
                    person_sets[row['person_id']].add(row[column.name])
                for person_id, local_ids in person_sets.items():
                    session.query(Person)\
                           .filter(id == row['person_id'])\
                           .update({column: local_ids})

                if Class != None:
                    session.query(Class).delete()
                    records = (Class(**row) for row in rows)
                    session.add_all(records)

        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())
    session.commit()

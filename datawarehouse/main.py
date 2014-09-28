import os
import csv
from collections import defaultdict

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from doeund import make_cubes
from .person import Person

file_mapping = [
    ('emailaddress.csv', 'email_addresses', EmailAddress),
    ('facebook.csv', 'facebooks', Facebook),
    ('twitter.csv', 'twitters', Twitter),
    ('name.csv', 'names', None),
    ('ipaddress.csv', 'ip_addresses', None),
    ('piwik.csv', 'piwiks', None),
]

def _strip(dictionary):
    return {k.strip():v.strip() for k,v in dictionary.items()}

def load(engine):
    directory = os.path.expanduser('~/git/dadawarehouse-manual')
    load_person(directory, engine)
    session = sessionmaker(engine)()

    for statement in make_cubes():
        session.execute(statement)
    session.commit()

def load_csv(directory, engine):
    session = sessionmaker(bind=engine)()
    for filename, column_name, Class in file_mapping:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))

                new_person_ids = set(row['person_id'] for row in rows) - \
                                 set(session.query(Person.id))
                session.add_all(Person(id = pid) for pid in new_person_ids)

                person_sets = defaultdict(lambda: set())
                for row in rows:
                    person_sets[row['person_id']].add(row['value'])
                for person_id, local_ids in person_sets.items():
                    session.query(Person)\
                           .filter(id = row['person_id'])\
                           .update({column_name: local_ids})

                if Class != None:
                    session.query(Class).delete()
                    records = (Class(person_id = row['person_id'],
                                     id = row['value'])\
                               for row in rows)
                    session.add_all(records)

        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())
    session.commit()

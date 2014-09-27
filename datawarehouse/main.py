import os
import csv

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from doeund import make_cubes
from .person import Facebook, EmailAddress, Person
from .fuzzy_person import Name, IPAddress

file_mapping = [
    ('facebook.csv', Facebook),
    ('name.csv', Name),
    ('emailaddress.csv', EmailAddress),
    ('ipaddress.csv', IPAddress),
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

def load_person(directory, engine):
    session = sessionmaker(bind=engine)()
    for filename, Class in file_mapping:
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))
                new_person_ids = set(row['person_id'] for row in rows) - \
                                 set(session.query(Person.id))
                session.add_all(Person(id = pid) for pid in new_person_ids)
                session.query(Class).delete()
                session.add_all(Class(**row) for row in rows)
        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())
    session.commit()

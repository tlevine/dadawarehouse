import os
import csv

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .person import Facebook, EmailAddress
from .fuzzy_person import Name, IPAddress

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

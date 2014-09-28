import os
import csv
from collections import Counter

from sqlalchemy.ext.declarative import declarative_base

from datamarts.logger import logger
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
    ('emailaddress.csv', EmailAddress),
    ('facebook.csv', Facebook),
    ('twitter.csv', Twitter),
    ('name.csv', None),
    ('ipaddress.csv', None),
    ('piwik.csv', None),
]

def load_person(session, directory):
    for filename, Class in file_mapping:
        logger.info('Importing %s' % filename)
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))

            new_person_ids = set(row['person_id'] for row in rows) - \
                             set(session.query(Person.id))
            session.add_all(Person(id = pid) for pid in new_person_ids)

            if Class != None and len(rows) > 0:
                column_name = list(set(rows[0].keys()) - {'person_id'})[0]
                counts = Counter(row[column_name] for row in rows)
                for value, count in counts.items():
                    if count > 1:
                        logger.warning('The value "%s" is duplicated in the "%s" column of "%s".' % (value, column_name, filename))

                session.query(Class).delete()
                records = (Class(**row) for row in rows)
                session.add_all(records)

            session.flush()

        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())

    session.commit()

def _strip(dictionary):
    return {k.strip():v.strip() for k,v in dictionary.items()}

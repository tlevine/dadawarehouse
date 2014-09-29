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

from .model import (
    Person,
    PersonEmailAddress, Facebook, Twitter,
    PersonName, PersonLocation, PiwikVisitor,
)

file_mapping = [
    ('emailaddress.csv', PersonEmailAddress),
    ('facebook.csv', Facebook),
    ('twitter.csv', Twitter),
    ('name.csv', PersonName),
    ('personlocation.csv', PersonLocation),
    ('piwik.csv', PiwikVisitor),
]

def load_person(session, directory):
    for filename, Class in file_mapping:
        logger.info('Importing %s' % filename)
        path = os.path.join(directory, filename)
        if os.path.exists(path):
            with open(path) as fp:
                rows = list(map(_strip, csv.DictReader(fp)))

            old_person_ids = set(row[0] for row in session.query(Person.id))
            new_person_ids = set(row['person_id'] for row in rows)
            session.add_all(Person(id = pid) for pid in \
                            (new_person_ids - old_person_ids))

            # Check for duplicates.
            msg = 'The following values are duplicated in the "%s" column of "%s":\n\n%s\n'
            for name, column in Class.__table__.columns.items():
                if column.unique:
                    values = list(duplicates(rows, name))
                    if len(values) > 0:
                        logger.warning(msg % (column_name, path, '\n'.join(values)))

            session.query(Class).delete()
            records = (Class(**row) for row in rows)
            session.add_all(records)

            session.flush()

        else:
            with open(path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(Class.__table__.columns.keys())

    session.commit()

def duplicates(rows, column_name):
    counts = Counter(row[column_name] for row in rows)
    for value, count in counts.items():
        if count > 1:
            yield value

def _strip(dictionary):
    return {k.strip():v.strip() for k,v in dictionary.items()}

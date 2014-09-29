import os

from sqlalchemy.orm import sessionmaker

from doeund import make_cubes

from .person.load_csv import load_person
from .person.load_sql import load_piwik

def load(engine):
    directory = os.path.expanduser('~/git/dadawarehouse-manual')
    session = sessionmaker(engine)()

    load_person(session, directory)
    load_piwik(session)

    for statement in make_cubes():
        session.execute(statement)
    session.commit()


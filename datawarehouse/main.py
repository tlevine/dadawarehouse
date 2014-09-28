import os

from sqlalchemy.orm import sessionmaker

from doeund import make_cubes

from .person.load import load_person

def load(engine):
    directory = os.path.expanduser('~/git/dadawarehouse-manual')
    session = sessionmaker(engine)()
    load_person(session, directory)

    for statement in make_cubes():
        session.execute(statement)
    session.commit()


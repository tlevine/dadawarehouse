import os

from doeund import make_cubes

from .person.load import load_person

def load(engine):
    directory = os.path.expanduser('~/git/dadawarehouse-manual')
    load_person(directory, engine)
    session = sessionmaker(engine)()

    for statement in make_cubes():
        session.execute(statement)
    session.commit()


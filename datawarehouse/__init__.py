import csv
import os

from sqlalchemy.orm import sessionmaker

from doeund import make_cubes

from .person import load as person

def load(engine):
    directory = os.path.expanduser('~/git/dadawarehouse-manual')
    person(directory, engine)
    session = sessionmaker(engine)()

    for statement in make_cubes():
        session.execute(statement)
    session.commit()

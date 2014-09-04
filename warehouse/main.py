import os

from sqlalchemy import create_engine

from doeund import doeund

from .history.load import update as history
from .pal.load import update as pal
#from .facebookchat.load import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def connect_sqlite(cache_directory):
    if not os.path.isdir(cache_directory):
        os.mkdir(cache_directory)
    database_file = os.path.join(cache_directory, 'dada.sqlite')
    engine = create_engine('sqlite:///' + database_file)
    return doeund(engine)

def load():
    session, _ = doeund(create_engine('postgres:///tlevine'))
   #fb(session)
    history(session)
    pal(session)

def query():
    _, cubes = doeund(create_engine('postgres:///tlevine'))
    return cubes

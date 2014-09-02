import os

from sqlalchemy import create_engine

from doeund import doeund

from .history import update as history
from .pal import update as pal
from .facebookchat import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def connect(cache_directory):
    if not os.path.isdir(cache_directory):
        os.mkdir(cache_directory)
    database_file = os.path.join(cache_directory, 'dada.sqlite')
    engine = create_engine('sqlite:///' + database_file)
    return doeund(engine)

def load():
    session, _ = connect(CACHE_DIRECTORY)
   #fb(session)
   #history(session)
    pal(session)

def query():
    session, cubes = connect(CACHE_DIRECTORY)

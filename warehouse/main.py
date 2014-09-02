import os

from doeund import doeund

from .history import update as history
from .pal import update as pal
from .facebookchat import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def connect(cache_directory):
    database_file = os.path.join(cache_directory, 'dada.sqlite')
    engine = s.create_engine('sqlite:///' + database_file)
    return doeund(engine)

def load():
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    session, _ = connect(CACHE_DIRECTORY)
   #fb(session)
   #history(session)
    pal(session)

def query():
    session, cubes = connect(CACHE_DIRECTORY)

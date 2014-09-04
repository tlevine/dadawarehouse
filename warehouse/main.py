import os

from sqlalchemy import create_engine

from doeund import doeund

from .history.load import update as history
from .pal.load import update as pal
#from .facebookchat.load import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    engine = create_engine('postgres:///tlevine')
    session, _ = doeund(engine)
   #fb(session)
    history(session)
    pal(session)

def query():
    _, cubes = doeund(create_engine('postgres:///tlevine'))
    return cubes

import os

from sqlalchemy import create_engine

from doeund import doeund

from .model import create_datetimes
from .history.load import update as history
from .pal.load import update as pal
#from .facebookchat.load import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    engine = create_engine('postgres:///tlevine')
    session, _ = doeund(engine)
    session.add_all(create_datetimes())
   #fb(session)
   #history(session)
    pal(session)

def query():
    _, cubes = doeund(create_engine('postgres:///tlevine'))
    return cubes

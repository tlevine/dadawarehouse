import os

from sqlalchemy import create_engine

from doeund import doeund

from warehouse.history.load import update as history
from warehouse.pal.load import update as pal
from warehouse.facebookchat.load import update as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
  # engine = create_engine('postgres:///tlevine')
    engine = create_engine('sqlite:////tmp/dada.sqlite')
    session, _ = doeund(engine)
   #fb(session)
    history(session)
    pal(session)

def example():
    _, cubes = doeund(create_engine('postgres:///tlevine'))
    cube = cubes['fact_facebookchatstatuschange'] #.dimensions['facebookuser']
    print('When Thomas Levines went online and offline:')
    print(cube.point_cut('facebookuser', ['Thomas Levine']).all())

if __name__ == '__main__':
    session, cubes = doeund(create_engine('postgres:///tlevine'))

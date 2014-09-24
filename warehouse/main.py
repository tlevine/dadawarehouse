import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import Base
from .pal.load import update as pal
from .history.load import update as history
from .gnucash.load import update as gnucash
from .facebookchat.load import update as fb
#from .twitter.load import update as twitter
#from .notmuch.load import update as notmuch

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load_data():
  # engine = create_engine('postgres:///tlevine')
    engine = create_engine('sqlite:////tmp/dada.sqlite')

    Base.metadata.create_all(engine) 
    session = sessionmaker(bind=engine)()

   #pal(session)
   #history(session)
   #gnucash(session)
    fb(session)
   #notmuch(session)

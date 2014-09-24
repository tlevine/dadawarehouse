import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import Base
from .pal.load import update as pal
from .history.load import update as history
from .gnucash.load import update as gnucash
from .facebookchat.load import update as fb
from .notmuch.load import update as notmuch
from .twitter.load import update as twitter
from .branchable.load import update as branchable
from .piwik.load import update as piwik

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')


def get_engine():
    return create_engine('postgres:///tlevine')
   #return create_engine('sqlite:////tmp/dada.sqlite')

def get_session():
    return sessionmaker(bind=get_engine())()

def load_data(engine = None):
    if engine == None:
        engine = get_engine()

    Base.metadata.create_all(engine) 
    session = sessionmaker(bind=engine)()

    piwik(session)
    return

    # Minutely updates
    history(session)
    notmuch(session)
    branchable(session)

    # Daily updates
    fb(session)

    # These delete existing state and thus take a while.
    # Also, the data aren't updated that often.
    # So we put them last.
    twitter(session)
    pal(session)
    gnucash(session)

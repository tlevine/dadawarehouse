import os

import warehouse.db as db
import warehouse.history as history
import warehouse.pal as pal

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    session = db.session(CACHE_DIRECTORY)
   #history.update(session)
    pal.update(session)

import os

import .db as db
import .history as history
import .pal as pal
import .facebookchat as fb

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    session = db.session(CACHE_DIRECTORY)
    fb.update(session)
   #history.update(session)
   #pal.update(session)

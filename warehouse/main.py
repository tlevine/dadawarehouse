import os

import history

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    history.run(CACHE_DIRECTORY)

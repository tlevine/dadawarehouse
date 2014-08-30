import os

import warehouse.history as h

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load():
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    h.run(CACHE_DIRECTORY)

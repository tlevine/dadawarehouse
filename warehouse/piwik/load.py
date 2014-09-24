import os

from ..util import i_should_copy
from .nfsn import mysqldump

LOCAL_DUMP = os.path.expanduser('~/.dadawarehouse/piwik.sql')
def update(session):
    if i_should_copy(LOCAL_DUMP):
        mysqldump(LOCAL_DUMP)

import os, subprocess, datetime

from sqlalchemy import desc

from ..util import i_should_copy
from ..logger import logger
from .parser import entry
from .model import BranchableLog

LOCAL_LOGDUMP = os.path.expanduser('~/.dadawarehouse/branchable-logdump')

def update(session):    
    if i_should_copy(LOCAL_LOGDUMP):
        copy_log(LOCAL_LOGDUMP)
    most_recent = session.query(BranchableLog.datetime)\
                  .order_by(desc(BranchableLog.datetime))\
                  .limit(1).scalar()
    try:
        with open(LOCAL_LOGDUMP) as fp:
            session.add_all(new_entries(fp, most_recent))
    except KeyboardInterrupt:
        pass
    else:
        session.commit()

def new_entries(fp, most_recent):
    for line in fp:
        if ' + pkBaseURL + ' in line:
            # This request came from a bot that is bad at parsing Javascript
            continue
        try:
            e = entry(line)
        except:
            logger.error('Error parsing this line, skipping:\n%s' % line)
        else:
            if most_recent == None or e.datetime >= most_recent:
                yield e

def copy_log(local_filename):
    command = ['ssh', 'b-thomaslevine@thomaslevine.branchable.com', 'logdump']
    with open(local_filename, 'w') as fp:
        sp = subprocess.Popen(command, stdout = fp)
        sp.wait()


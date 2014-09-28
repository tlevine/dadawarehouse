import os, subprocess, datetime
from functools import partial

from sqlalchemy import desc

from ..util import i_should_copy
from ..logger import logger
from .parser import entry
from .model import BranchableLog

LOCAL_LOGDUMP_DIR = os.path.expanduser('~/.dadawarehouse/branchable-logdump')

def update(session):    
    os.makedirs(LOCAL_LOGDUMP_DIR, exist_ok = True)
    new_logdump_file = os.path.join(LOCAL_LOGDUMP_DIR, datetime.date.today().isoformat())
    if i_should_copy(new_logdump_file):
        copy_log(new_logdump_file)
    most_recent = session.query(BranchableLog.datetime)\
                  .order_by(desc(BranchableLog.datetime))\
                  .limit(1).scalar()

    for logdump_file in map(partial(os.path.join, LOCAL_LOGDUMP_DIR), os.listdir(LOCAL_LOGDUMP_DIR)):
        try:
            with open(logdump_file) as fp:
                session.add_all(new_entries(fp, most_recent))
        except KeyboardInterrupt:
            break

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


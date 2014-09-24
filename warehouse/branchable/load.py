import os, subprocess, datetime

LOCAL_LOGDUMP = os.path.expanduser('~/.dadawarehouse/branchable-logdump')

def update(session):    
    if i_should_copy_the_log(LOCAL_LOGDUMP):
        copy_log(LOCAL_LOGDUMP)
    with open(LOCAL_LOGDUMP) as fp:
        for e in entries(fp):
            print(e)
       #session.add_all(new_entries(entries(fp)))


def entries(fp):
    for line in fp:
        yield 

def new_entries(entries, most_recent):
    for entry in entries:
#       if entry['datetime'] >= most_recent:
            yield entry


def i_should_copy_the_log(local_filename):
    if not os.path.exists(local_filename):
        return True

    mtime = datetime.datetime.fromtimestamp(os.stat(local_filename).st_mtime)
    a_day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)
    return mtime < a_day_ago

def copy_log(local_filename):
    command = ['ssh', 'b-thomaslevine@thomaslevine.branchable.com', 'logdump']
    with open(local_filename, 'w') as fp:
        sp = subprocess.Popen(command, stdout = fp)
        sp.wait()


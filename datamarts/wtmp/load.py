from subprocess import Popen, PIPE

from .model import Last

def update(session):
    for host in ['nsa', 'home']:
        for filename in ls(host):
            records = (Last.factory(host, filename, line) for line in last(host, filename))
            session.add_all(records)
            session.commit()

def shell(f):
    def wrapper(*args, **kwargs):
        command = f(*args, **kwargs)
        sp = Popen(command, stdout = PIPE, stderr = PIPE)
        stdout, stderr = sp.communicate()
        sp.wait()
        return filter(None, stdout.decode('utf-8').split('\n'))
    return wrapper

@shell
def ls(host):
    return ['ssh', host, 'ls /var/log/wtmp*']

@shell
def last(host, filename):
    return ['ssh', host, "last -w -F -a -f '%s'" % filename]

from subprocess import Popen, PIPE

from ..logger import logger

from .model import Last

def update(sessionmaker):
    session = sessionmaker()
    for host in ['nsa', 'home']:
        session.query(Last).filter(Last.computer == host).delete()
        session.flush()
        for filename in ls(host):
            records = (Last.factory(host, filename, line) for line in last(host, filename))
            session.add_all(records)
        session.commit()
        logger.debug('Imported last logs from %s' % host)

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

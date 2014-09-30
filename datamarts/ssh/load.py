from subprocess import Popen, PIPE

def update(session):
    for host in ['nsa', 'home']:
        for filename in ls(host):
            print(host, filename)
            print(len(list(last(host, filename))))


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
    return ['ssh', host, "last -F -a -f '%s'" % filename]

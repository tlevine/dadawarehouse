from subprocess import Popen, PIPE

def shell_command(f):
    def wrapper(*args, **kwargs):
        command = f(*args, **kwargs)
        sp = Popen(command, stdout = PIPE, stderr = PIPE)
        sp.wait()
        stdout, stderr = sp.communicate()
        return stdout.split('\n')
    return wrapper

def ls(host):
    return ['ssh', host, 'ls /var/log/wtmp*']

def last(host, filename):
    return ['ssh', host, "last -F -a -f '%s'" % filename]

for filename in ls('nsa'):
    print(last('nsa', filename))

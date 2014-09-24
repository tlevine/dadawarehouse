import os, subprocess

def mysqldump(local_filename):
    key = 'NFSN_PIWIK_EXPORT_PASSWORD'
    if key not in os.environ:
        raise EnvironmentError('You must set the %s variable' % key)

    remote_command = 'mysqldump --host=thomaslevine.db ' \
                     '--user=export --password=\'%s\' piwik' % \
                     os.environ[key]

    with open(local_filename, 'w') as fp:
        ssh = subprocess.Popen(['ssh', 'piwik', remote_command], stdout = fp)
        ssh.wait()

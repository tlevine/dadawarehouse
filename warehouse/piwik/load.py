import os, subprocess

from ..util import i_should_copy

DB_DUMP_FILENAME = os.path.expanduser('~/.dadawarehouse/piwik.sql')

def update(session):
    if i_should_copy(DB_DUMP_FILENAME):
        mysqldump(DB_DUMP_FILENAME)
        restore(DB_DUMP_FILENAME)

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

def restore(local_filename):
    sql = 'CREATE DATABASE IF NOT EXISTS piwik;'
    subprocess.Popen(['echo', sql, '|', 'mysql', '-uroot']).wait()
    with open(local_filename) as fp:
        subprocess.Popen(['mysql', '-uroot', 'piwik'], stdin = fp).wait()

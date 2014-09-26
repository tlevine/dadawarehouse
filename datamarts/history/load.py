import subprocess
import os
import shlex

from historian_reader.shell import historian

import doeund as m
from ..logger import logger
from .model import ShellSession, ShellCommand

HISTORY = os.path.join(os.path.expanduser('~'), 'history')

def download():
    RSYNC = ['rsync', '--archive', '--sparse']
    remotes = ['history-nsa', 'history-home', 'history-laptop']
    rsync = subprocess.Popen(RSYNC + remotes + [HISTORY])
    rsync.wait()

def update(session):
    download()
    shell_history = os.path.join(HISTORY, 'shell')
    previous_shells = (row[0] for row in session.query(ShellSession.filename))
    for log in historian(directory = shell_history, skip = previous_shells):
        shell_session = ShellSession(filename = log['session'],
                                     datetime = log['session_date'])
        todo = [shell_session]
        for command_datetime, command_string in log['commands']:
            command = ShellCommand(
                shellsession = shell_session,
                datetime = command_datetime,
                full_command = command_string)
            todo.append(command)

        session.add_all(todo)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

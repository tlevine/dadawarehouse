import os
import shlex

from historian_reader.shell import historian

import doeund as m
from ..logger import logger
from .model import ShellSession, ShellCommand

def update(session):
    HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
    previous_shells = (row[0] for row in session.query(ShellSession.filename))
    for log in historian(directory = HISTORY, skip = previous_shells):
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

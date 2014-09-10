import os
import shlex

from historian_reader.shell import historian

import warehouse.model as m
from ..logger import logger
from .model import ShellSession, Command, CommandBody

def update(session):
    HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
    previous_shells = (row[0] for row in session.query(ShellSession.filename))
    for log in historian(directory = HISTORY, skip = previous_shells):
        shell_session = ShellSession(filename = log['session'],
                                     datetime = log['session_date'])
        for command_datetime, command_string in log['commands']:
            command = Command(datetime = command_datetime,
                              command = command_body).merge(session)
            shell_session.commands.append(command)
        shell_session.merge(session)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

import os

from historian_reader.shell import historian

import warehouse.model as m
from ..logger import logger
from .model import ShellSession, Command

def update(session):
    HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
    previous_shells = (row[0] for row in session.query(ShellSession.filename))
    for log in historian(directory = HISTORY, skip = previous_shells):
        shell_session = ShellSession(filename = log['session'],
                                     datetime = log['session_date'])
        for command_datetime, command_string in log['commands']:
            shell_session.commands.append(
                Command(datetime = command_datetime,
                        command = command_string))
        session.add(shell_session)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

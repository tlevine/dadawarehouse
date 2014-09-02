import os

from historian_reader.shell import historian

from .db import Command, Shell
from .logger import logger

def update(session):
    HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
    previous_shells = (row[0] for row in session.query(Shell.shell))
    for shell in historian(directory = HISTORY, skip = previous_shells):
        session.add(Shell(shell = shell['session'],
                          shell_date = shell['session_date']))
        session.add_all((Command(shell = shell['session'],
                                 command_date = command_date,
                                 command = command_string,
                ) for command_date, command_string in shell['commands']))
        session.commit()
        logger.info('Inserted commands from shell "%s"' % shell['session'])

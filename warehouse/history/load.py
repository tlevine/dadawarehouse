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
        datetime = m.DateTime(pk = log['session_date']).link(session)
        shell_session = ShellSession(filename = log['session'], datetime = datetime)
        for command_datetime, command_string in log['commands']:
            datetime = m.DateTime(pk = command_datetime).link(session)
            command = Command(datetime = datetime), command = command_body).link(session)
            shell_session.commands.append(command)
        session.add(shell_session)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

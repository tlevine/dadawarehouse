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
        todo = []
        shell_session = session.merge(ShellSession(
            filename = log['session'], datetime_id = log['session_date']))
        for command_datetime, command_string in log['commands']:
            command_id = CommandBody.from_label(session, command_string)
            command = Command(datetime_id = command_datetime,
                              shellsession = shell_session,
                              command_id = command_id)
            todo.append(command)

        session.add(shell_session)
        ShellSession.create_related(session)
        session.add_all(todo)
        Command.create_related(session)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

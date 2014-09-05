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
            command_body = session.query(CommandBody)\
               .filter(CommandBody.full_command == command_string).first()
            if command_body == None:
                arg0, arg1, arg2 = (shlex.split(command_string) + [None] * 3)[:3]
                command_body = CommandBody(arg0 = arg0, arg1 = arg1,
                    arg2 = arg2, full_command = command_string)
                session.add(command_body)
                session.commit()
            shell_session.commands.append(
                Command(datetime = command_datetime,
                        command = command_body))
        session.add(shell_session)
        session.commit()
        logger.info('Inserted commands from shell "%s"' % log['session'])

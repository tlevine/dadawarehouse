import shlex
import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as m
from ..logger import logger

def _arg(n, max_n = 3):
    'Make a "default" function that returns the n-th arg.'
    def default(context):
        command_string = context.current_parameters['full_command']
        try:
            args = (shlex.split(command_string) + [None] * max_n)[:max_n]
        except ValueError:
            logger.warning('Error parsing command:\n %s' % command_string)
        else:
            return args[n]
    return default

class ShellSession(m.Dimension):
    pk = m.PkColumn(hide = True)
    datetime = m.Column(s.DateTime, label = 'Session start')
    filename = m.Column(s.String, label = 'File Name')

class ShellCommand(m.Fact):
    pk = m.PkColumn(hide = True)
    shellsession_id = m.FkColumn(ShellSession.pk)
    shellsession = relationship(ShellSession)
    datetime = m.Column(s.DateTime, label = 'Command run')
    arg0 = m.Column(s.String, nullable = True, label = '$0', default = _arg(0))
    arg1 = m.Column(s.String, nullable = True, label = '$1', default = _arg(1))
    arg2 = m.Column(s.String, nullable = True, label = '$2', default = _arg(2))
    full_command = m.Column(s.String, label = '!!')

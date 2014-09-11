import shlex
import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension, Fact

import warehouse.model as m

def _arg(n, max_n = 3):
    'Make a "default" function that returns the n-th arg.'
    def default(context):
        command_string = context.current_parameters['full_command']
        args = (shlex.split(command_string) + [None] * max_n)[:max_n]
        return args[n]
    return default

class CommandBody(Dimension):
    pk = m.PkColumn()
    arg0 = m.Column(s.String, nullable = True, label = '$0', default = _arg(0))
    arg1 = m.Column(s.String, nullable = True, label = '$1', default = _arg(1))
    arg2 = m.Column(s.String, nullable = True, label = '$2', default = _arg(2))
    full_command = m.Column(s.String, unique = True, label = '!!')

class ShellSession(Dimension):
    pk = m.PkColumn()
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    filename = m.LabelColumn(label = 'File Name')

class Command(Fact):
    pk = m.PkColumn()
    shellsession_id = m.FkColumn(ShellSession.pk)
    shellsession = relationship(ShellSession)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    command_id = m.FkColumn(CommandBody.pk)
    command = relationship(CommandBody)

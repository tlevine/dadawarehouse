import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class CommandBody(d.Dimension):
    pk = m.PkColumn()
    arg0 = m.Column(s.String, nullable = True, label = '$0')
    arg1 = m.Column(s.String, nullable = True, label = '$1')
    arg2 = m.Column(s.String, nullable = True, label = '$2')
    full_command = m.Column(s.String, unique = True, label = '!!')

class ShellSession(d.Dimension):
    pk = m.PkColumn()
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    filename = m.LabelColumn(label = 'File Name')
    commands = relationship('Command')

class Command(d.Fact):
    pk = m.PkColumn()
    shellsession_id = m.FkColumn(ShellSession.pk)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    command_id = m.FkColumn(CommandBody.pk)
    command = relationship(CommandBody)

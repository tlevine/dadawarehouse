import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class CommandBody(m.Dimension):
    pk = m.PkColumn()
    arg0 = m.Column(s.String, nullable = True)
    arg1 = m.Column(s.String, nullable = True)
    arg2 = m.Column(s.String, nullable = True)
    full_command = m.Column(s.String, unique = True)

class ShellSession(m.Dimension):
    pk = m.PkColumn()
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    filename = m.LabelColumn()
    commands = relationship('Command')

class Command(m.Fact):
    pk = m.PkColumn()
    shellsession_id = m.FkColumn(ShellSession.pk)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    command_id = m.FkColumn(CommandBody.pk)
    command = relationship(CommandBody)

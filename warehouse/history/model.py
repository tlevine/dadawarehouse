import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class CommandBody(m.Dimension):
    pk = m.PkColumn()
    arg0 = Column(s.String, nullable = True)
    arg1 = Column(s.String, nullable = True)
    arg2 = Column(s.String, nullable = True)
    full_command = Column(s.String, unique = True)

class ShellSession(m.Dimension):
    pk = m.PkColumn()
    datetime = m.Column(s.DateTime)
    filename = m.LabelColumn()
    commands = relationship('Command')

class Command(m.Fact):
    pk = m.PkColumn()
    shellsession_id = m.FkColumn(ShellSession.pk)
    datetime = m.Column(s.DateTime)
    command_id = FkColumn(CommandBody.pk)
    command = relationship(CommandBody)

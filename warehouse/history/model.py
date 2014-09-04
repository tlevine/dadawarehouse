import sqlalchemy as s
from sqlalchemy.orm import relationship, backref

import ..model as m

class ShellSession(m.Dimension):
    pk = m.PkColumn()
    date = m.DateColumn()
    time = m.TimeColumn()
    filename = m.LabelColumn()
    commands = relationship('Command')

class CommandString(m.Dimension):
    pk = m.PkColumn()
    command = m.LabelColumn()

class Command(m.Fact):
    pk = m.PkColumn()
    shell_id = m.FkColumn(ShellSession.pk)
    date_id = m.DateColumn()
    time_id = m.TimeColumn()
    command_id = m.FkColumn(CommandString.pk)

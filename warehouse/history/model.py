import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class ShellSession(m.Dimension):
    pk = m.PkColumn()
    datetime_id = m.DateTimeColumn()
    filename = m.LabelColumn()
    commands = relationship('Command')

class Command(m.Fact):
    pk = m.PkColumn()
    shellsession_id = m.FkColumn(ShellSession.pk)
    datetime_id = m.DateTimeColumn()
    command = m.Column(s.String)

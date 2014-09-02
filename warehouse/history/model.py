import sqlalchemy as s

from ..model import Fact, Dimension, Column, PkColumn, FkColumn, LabelColumn, Date, Time

class ShellFilename(Dimension):
    pk = PkColumn()
    filename = LabelColumn()

class ShellSession(Dimension):
    pk = IdColumn(primary_key = True, s.ForeignKey(ShellFilename.pk))
    date = Column(s.Date, s.ForeignKey(Date.pk))
    time = Column(s.Time, s.ForeignKey(Time.pk))

class CommandString(Dimension):
    pk = PkColumn()
    command = LabelColumn()

class Command(Fact):
    pk = PkColumn()
    shell = FkColumn(ShellSession.shell)
    date = Column(s.Date, s.ForeignKey(Date.pk))
    time = Column(s.Time, s.ForeignKey(Time.pk))
    command = FkColumn(CommandString)

import sqlalchemy as s

from .model import Fact, Dimension, Column, IdColumn, Date, Time

class ShellFilename(Dimension):
    pk = IdColumn(primary_key = True)
    filename = Column(s.String, unique = True)

class ShellSession(Dimension):
    pk = IdColumn(primary_key = True, s.ForeignKey(ShellFilename.pk))
    date = Column(s.Date, s.ForeignKey(Date.pk))
    time = Column(s.Integer, s.ForeignKey(Time.pk))

class CommandString(Dimension):
    pk = IdColumn(primary_key = True)
    command = Column(s.String, unique = True)

class Command(Fact):
    pk = IdColumn(s.Integer)
    shell = IdColumn(s.ForeignKey(ShellSession.shell))
    date = Column(s.Date, s.ForeignKey(Date.pk))
    time = Column(s.Integer, s.ForeignKey(Time.pk))
    command = IdColumn(s.ForeignKey(CommandString))

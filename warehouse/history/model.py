import sqlalchemy as s

from ..model import Fact, Dimension, Column, PkColumn, FkColumn, LabelColumn, Date, Time

class ShellSession(Dimension):
    pk = PkColumn()
    date = DateColumn()
    time = TimeColumn()
    filename = LabelColumn()

class CommandString(Dimension):
    pk = PkColumn()
    command = LabelColumn()

class Command(Fact):
    pk = PkColumn()
    shell = FkColumn(ShellSession.pk)
    date = DateColumn()
    time = TimeColumn()
    command = FkColumn(CommandString.pk)

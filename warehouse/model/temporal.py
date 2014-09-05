import sqlalchemy as s

from doeund import Fact, Dimension

from .base import Column, PkColumn, FkColumn, LabelColumn

class Day(Dimension):
    pk = Column(s.Date, 

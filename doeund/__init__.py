from .base import Base, Fact, Dimension, Helper
from .columns import Column, PkColumn, FkColumn
from .util import d

def make_cubes():
    return _export(Base.metadata.tables)

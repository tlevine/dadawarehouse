from .base import Base, Fact, Dimension, Helper
from .columns import Column, PkColumn, FkColumn
from .util import d
from .export import make_cubes as _make_cubes

def make_cubes():
    return _make_cubes(Base.metadata.tables)

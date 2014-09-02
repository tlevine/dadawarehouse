from collections import namedtuple
from enum import Enum

from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

Base = _declarative_base()

class Column(_Column):
    '''
    Column in a table, with model metadata

    This is a normal SQLAlchemy column with two special keyword arguments.

    label: pretty label for the field
    aggregations: list of aggregation functions
    '''
    def __init__(self, *args, **kwargs):
        _kwargs = dict(kwargs) # copy it rather than mutating it
        if 'label' in _kwargs:
            self.__label__ = _kwargs.pop('label')
        if 'aggregations' in _kwargs:
            self.__aggregations__ = _kwargs.pop('aggregations')
        _Column.__init__(self, *args, **_kwargs)

class Fact(Base):
    '''
    Dimensions and joins will be inferred based on foreign keys.
    I think we can do without mappings.
    http://pythonhosted.org/cubes/backends/sql.html#explicit-mapping
    '''
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'fact_' + Class.__name__.lower()

class Dimension(Base):
    '''
    What's info?

    levels are inferred from columns.

    __hierarchies__ is a list of cubes.models.Hierarchy objects
    '''
    __abstract__ = True
    __hierarchies__ = []

    @declared_attr
    def __tablename__(Class):
        return 'dim_' + Class.__name__.lower()

from collections import namedtuple
from enum import Enum

from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

from .inference import dim_levels, fact_measures, joins

Base = _declarative_base()

class Column(_Column):
    '''
    Column in a table with some model metadata

    This is a normal SQLAlchemy column with two special keyword arguments.

    label: pretty label for the field
    aggregations: list of aggregation functions
    '''
    def __init__(self, *args, **kwargs):
        _kwargs = dict(kwargs) # copy it rather than mutating it
        info = _kwargs.pop('info', {})
        if 'label' in _kwargs:
            info['label'] = _kwargs.pop('label')
        if 'aggregations' in _kwargs:
            info['aggregations'] = _kwargs.pop('aggregations')
        _Column.__init__(self, *args, info = info, **_kwargs)

class Fact(Base):
    '''
    A fact table
    '''
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'fact_' + Class.__name__.lower()

#   def __repr__(self):
#       msg = '<Fact "%s" with measures %s and referencing dimensions %s>'
#       measures = list(fact_measures(self.__table__).keys())
#       dimensions = list(to_column.table.name for (_, to_column) in joins(self.__table))
#       return msg % (self.__tablename__, measures, dimensions)

class Dimension(Base):
    '''
    A dimension table

    Each dimension table should have only one dimension;
    the different columns within that table are treated
    as a hierarchy of levels within that dimension.
    '''
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'dim_' + Class.__name__.lower()

#   def __repr__(self):
#       msg = '<Dimension "%s" with levels %s and referencing dimensions %s>'
#       measures = dim_levels(self.__table__)
#       dimensions = list(to_column.table.name for (_, to_column) in \
#                         joins(self.__table))
#       return msg % (self.__tablename__, measures, dimensions)

from collections import namedtuple
from enum import Enum

from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

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

    def merge(self, session):
        raise NotImplementedError(
            'Please implement a %(c)s.merge method that calls one of'
            '%(c)s._merge_label and %(c)s._merge_pk and that calls'
            '%(c)s._merge_references if it is appropriate.' % \
            {'c': self.__class__})

    def _merge_pk(self, session):
        return session.merge(self)

    def _merge_label(self, session, column_names):
        Class = self.__class__
        unique_columns = [getattr(Class, column_name) \
                          for column_name in column_names]
        values = [getattr(self, column_name) for column_name in column_names]
        for unique_column, value in zip(unique_columns, values):
            if unique_column == None:
                raise ValueError('The table doesn\'t have a %s column.' % column_name)
            elif value == None:
                raise ValueError('The instance doesn\'t have a %s attribute.' % column_name)
        else:
            return merge_on_unique(Class, session, unique_column, value)

def merge_on_unique(Class, session, unique_column, value, **kwargs):
    '''
    Merge on a single unique column, assuming that that is the only
    column in the table that needs to be specified.
    '''
    if value == None:
        raise ValueError('Value may not be None.')
    x = session.query(Class).filter(unique_column == value).first()
    if x == None:
        _kwargs = dict(kwargs)
        kwargs[unique_column.name] = value
        x = Class(**_kwargs)
        session.add(x)
    return x

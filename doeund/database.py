from collections import namedtuple
from enum import Enum

from sqlalchemy.orm import class_mapper
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

    def link(session):
        for relationship in class_mapper(self).relationships:
            if len(relationship).local_columns != 1:
                msg = 'Linking works only on relationships with one local column.'
                raise NotImplementError(msg)
            else:
                local_column = next(iter(relationship.local_columns))
                names = {
                    'relationship': relationship.key,
                    'foreign_key': local_column.key,
                    'reference': next(iter(local_column.foreign_keys)).column.name,
                }
                values = {
                    'relationship': getattr(self, names['relationship']).link(session),
                    'foreign_key': getattr(values['relationship'], names['reference'])
                }

                setattr(self, names['foreign_key'], values['foreign_key'])
                setattr(self, names['relationship'], None)
        

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

def merge_on_unique(Class, session, unique_column, value):
    '''
    Merge on a single unique column, assuming that that is the only
    column in the table that needs to be specified.
    '''
    if value == None:
        raise ValueError('Value may not be None.')
    x = session.query(Class).filter(unique_column == value).first()
    if x == None:
        x = Class(**{unique_column.name: value})
        session.add(x)
    return x

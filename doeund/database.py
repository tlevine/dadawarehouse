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

class DadaBase(Base):
    __abstract__ = True

    def link(self, session):
        table = class_mapper(self.__class__)
        if len(table.relationships) == 0:
            self = self._merge(session)
        else:
            for foreign_key in table.columns:
                for reference in foreign_key.foreign_keys:
                    self = self._link_one(session, foreign_key, reference)

        return self

    def _merge(self, session):
        return session.merge(self)

    def _link_one(self, session, foreign_key, reference):
        if reference.column.table.primary_key != (reference,):
            raise NotImplementedError('Only single-column primary keys are supported.')
        else:
            Table = class_mapper(reference.table.__class__)
            pk_name = reference.name
            pk_value = getattr(self, foreign_key.name)

            other_table = Table(**{pk_name: pk_value}).link(session)
            setattr(self, foreign_key.name, getattr(other_table, pk_name))

        return self

class Fact(DadaBase):
    '''
    A fact table
    '''
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'fact_' + Class.__name__.lower()

class Dimension(DadaBase):
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

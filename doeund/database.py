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
            out = self._merge(session)
        else:
            for relationship in table.relationships:
                self = self._link_one(session, relationship)
            out = self
        return out


    _existing_references = set()

    def _merge(self, session):
        primary_key_columns = [c.name for c in self.__table__.columns if c.primary_key]
        unique_columns = [c.name for c in self.__table__.columns if c.unique]

        if len(primary_key_columns) > 1 or len(unique_columns) > 1:
            raise NotImplementedError
        elif len(unique_columns) == 1:
            primary_key = False
            unique_column = unique_columns[0]
        elif len(primary_key_columns) == 1:
            primary_key = True
            unique_column = primary_key_columns[0]
        else:
            raise NotImplementedError

        Class = self.__class__
        value = getattr(self, unique_column)

        if False: # value in Class._existing_references:
            return self
        elif primary_key:
            Class._existing_references.add(value)
            return session.merge(self)
        else:
            Class._existing_references.add(value)
            return merge_on_unique(Class, session, getattr(Class, unique_column), value)

    def _link_one(self, session, relationship):
        if len(relationship.local_columns) != 1:
            msg = 'Automatic linking is not implemented for relationships with local column counts other than one.'
            raise NotImplementedError(msg)
        else:
            local_column = next(iter(relationship.local_columns))
            names = {
                'relationship': relationship.key,
                'foreign_key': local_column.key,
                'reference': next(iter(local_column.foreign_keys)).column.name,
            }

            related_instance = getattr(self, names['relationship'])
            if related_instance == None:
                msg = 'You must set the relationship attribute, not the foreign key attribute, for automatic linking to work.'
                raise NotImplementedError(msg)
            target = getattr(related_instance.link(session), names['reference'])
            
            setattr(self, names['foreign_key'], target)
            setattr(self, names['relationship'], None)
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

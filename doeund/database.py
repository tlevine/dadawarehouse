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

class DadaBase(Base):
    __abstract__ = True

    def merge(self, session):
        'Merge the present instance and all of its references into the session.'
        if len(list(self._uniques())) > 0:
            return self._merge_label(session)
        else:
            return self._merge_pk(session)

    @classmethod
    def _relationships(Class):
        for r in Class.__mapper__.relationships:
            if len(r.local_columns) != 1:
                msg = 'The relationship must have exactly one local column.'
                raise ValueError(msg)
            yield next(iter(r.local_columns)).name, r.key, r.argument

    @classmethod
    def _uniques(Class):
        for c in Class.__mapper__.columns:
            if c.unique:
                yield c.name 

    def _merge_pk(self, session):
        for colname, relname, Class in self.__class__._relationships():
            r = getattr(self, relname)

            if r == None:
                r = Class(pk = getattr(self, colname))

            if r == None:
                raise ValueError('The reference %s.%s and its column, %s.%s,'
                    'are both None (not defined). This isn\'t allowed.' % \
                    (self, relname, self, colname))

            setattr(self, relname, r.merge(session))

        return session.merge(self)

    def _merge_label(self, session):
        Class = self.__class__
        filters = [(getattr(Class, column_name), getattr(self, column_name)) \
                   for column_name in self._uniques()]

        query = session.query(Class)
        for unique_column, value in filters:
            query = query.filter(unique_column == value)

        record = query.first()
        if record == None:
            columns = self.__table__.columns
            kwargs = {column.name: getattr(self, column.name) for column in columns}
            record = Class(**kwargs)
            record = session.add(record)
            session.commit()

        return record


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

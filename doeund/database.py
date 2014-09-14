from logging import getLogger
logger = getLogger('doeund')

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

    @classmethod
    def _uniques(Class):
        return [c for c in Class.__mapper__.columns if c.unique]

    @classmethod
    def _primary_keys(Class):
        return [c for c in Class.__mapper__.columns if c.primary_key]

    @classmethod
    def from_label(Class, session, *values):
        '''
        This returns the primary key, creating the record if needed.

        The values are specified in the order of the table.
        '''
        values = tuple(values)
        primary_keys = Class._primary_keys()
        if len(primary_keys) != 1:
            raise TypeError('To use %(c)s.from_label, %(c)s must have exactly one primary key column, not %(n)s' % {'c': Class.__name__, 'n': len(primary_keys)})
        primary_key = primary_keys[0]

        uniques = Class._uniques()
        if len(uniques) != len(values):
            raise TypeError('You must provide as many values as their are uniques in %(c)s (%(n)d values)' % {'c': Class.__name__, 'n': len(uniques)})

        if not hasattr(Class, '_label_mapping'):
            Class._label_mapping = {}
            for instance in session.query(Class):
                key = tuple(getattr(instance, name) for name in uniques)
                Class._label_mapping[key] = getattr(instance, primary_key.name)

        if values not in Class._label_mapping:
            if len(Class._label_mapping) == 0:
                primary_key_value = 1
            else:
                primary_key_value = max(Class._label_mapping.values()) + 1
            kwargs = {unique.name: value for unique, value in zip(uniques, values)}
            kwargs[primary_key.name] = primary_key_value
            instance = Class(**kwargs)
            session.add(instance)
            Class._label_mapping[values] = primary_key_value

        return Class._label_mapping[values]

    @classmethod
    def create_related(Class, session):
        '''
        Create entries in related tables.
        '''
        for relationship in Class.__mapper__.relationships:

            if len(relationship.local_columns) != 1:
                msg = 'The relationship must have exactly one local column.'
                raise ValueError(msg)

            from_column = list(relationship.local_columns)[0]
            to_columns = (fk.column for fk in from_column.foreign_keys)

            for to_column in to_columns:
                if not to_column.primary_key:
                    msg = 'Skipping %s because it is not a primary key'
                    logger.debug(msg % to_column.name)
                    continue
                elif any(c.unique for c in to_column.table.columns):
                    msg = 'Skipping %s because it is for a label table'
                    logger.debug(msg % to_column.name)
                    continue
                elif to_column.table != relationship.target:
                    msg = 'Skipping %s because is a different reference' \
                          'from the same foreign key relationship column'
                    logger.debug(msg % to_column.name)
                    continue

                from_values = set(v[0] for v in session.query(from_column).distinct())
                to_values = set(v[0] for v in session.query(to_column).distinct())
                values = from_values - to_values
                f = lambda value: relationship.argument(**{to_column.name: value})

                logger.debug(to_column)
                logger.debug(relationship.argument)
                logger.debug('From values: %s' % list(sorted(from_values)))
                logger.debug('To values: %s' % list(sorted(to_values)))
                logger.debug('Adding these values: %s' % list(sorted(values)))
                logger.debug('')

                session.add_all(map(f, values))

            relationship.argument.create_related(session)

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

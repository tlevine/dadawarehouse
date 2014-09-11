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
    def _relationships(Class):
        for r in Class.__mapper__.relationships:
            if len(r.local_columns) != 1:
                msg = 'The relationship must have exactly one local column.'
                raise ValueError(msg)
            yield next(iter(r.local_columns)).name, r.key, r.argument

    @classmethod
    def _uniques(Class):
        return [c.name for c in Class.__mapper__.columns if c.unique]

    @classmethod
    def _primary_keys(Class):
        return [c.name for c in Class.__mapper__.columns if c.primary_key]

    _label_mapping = {}
    @classmethod
    def from_label(Class, session, value):
        'Returns the primary key, creating the record if needed'
        uniques = Class._uniques()
        if len(uniques) != 1:
            raise TypeError('To use %(c)s.from_label, %(c)s must have exactly one unique column, not %(n)s' % {'c': Class.__name__, 'n': len(uniques)})
        unique = uniques[0]

        primary_keys = Class._primary_keys()
        if len(primary_keys) != 1:
            raise TypeError('To use %(c)s.from_label, %(c)s must have exactly one primary key column, not %(n)s' % {'c': Class.__name__, 'n': len(primary_keys)})
        primary_key = primary_keys[0]

        if len(Class._label_mapping) == 0:
            for instance in session.query(Class):
                Class._label_mapping[getattr(instance, unique.name)] = getattr(instance, primary_key.name)

        if value not in Class._label_mapping:
            primary_key_value = max(Class._label_mapping.values())
            kwargs = {primary_key.name: primary_key_value, unique.name: value}
            instance = Class(**kwargs)
            session.add(instance)
            Class._label_mapping[value] = primary_key_value

        return Class._label_mapping[value]

    @classmethod
    def create_reference(Class, session, column_name):
        from_column = Class.__table__[column_name]
       #list(list(warehouse.pal.model.CalendarEvent.__table__.columns)[1].foreign_keys)[0].column
       #list(list(warehouse.pal.model.CalendarEvent.__table__.columns)[1].foreign_keys)[0].column
        to_columns = (fk.column for fk in to_column.foreign_keys)
        for to_column in to_columns:
            from_values = set(session.query(from_column).distinct())
            to_values = set(session.query(to_column).distinct())
            for value in to_values - from_values:
                to_column.table(**{to_column.name: value})

    @classmethod
    def create_related(ParentClass, session):
        raise NotImplementedError
        # With each relationship,
        for colname, relname, Class in ParentClass._relationships():
            # look through all of the values of the foreign key column,
            # that aren't in the referenced table
            import pdb; pdb.set_trace()
            reference = session.query(getattr(Class, 'pk'))

            # Where can I get pkname?
            # Perhaps relationships may only involve primary key columns...
            # Can I do this with foreign keys and without relationships?
            parent = session.query(getattr(ParentClass, colname)).distinct()
           #pks = (for pk in set(reference) - set(parent))

            session.add_all(Class(pk = pk) for pk in pks)
            session.commit()
            Class.create_related(session)

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

from collections import namedtuple

from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import declarative_base as _declarative_base

Base = _declarative_base()

class ModelColumn(_Column):
    'Column in a table, with model metadata'
    def __init__(self, *args, **kwargs):
        _kwargs = dict(kwargs) # copy it rather than mutating it
        if 'label' in _kwargs:
            self.__label__ = _kwargs.pop('label')
        _Column.__init__(self, *args, **_kwargs)

class Measure(ModelColumn):
    __aggregations__ = []

class ModelTable(Base):
    __label__ = None

class Dimension(ModelTable):
    '''
    What's info?

    levels are inferred from columns.

    __hierarchies__ is a list of cubes.models.Hierarchy objects
    '''
    __hierarchies__ = []

    @classmethod
    def levels(Class):
        '''
        Everything that isn't a primary key is a level.'
        '''
        return filter(lambda column: not column.primary_key, Class.__table__.columns)

class Fact(ModelTable):
    '''
    Dimensions and joins will be inferred based on foreign keys.
    I think we can do without mappings.
    http://pythonhosted.org/cubes/backends/sql.html#explicit-mapping
    '''
    @classmethod
    def measures(Class):
        '''
        List the columns that are not foreign keys.
        '''
        return filter(lambda column: len(column.foreign_keys) == 0, Class.__table__.columns)

    @classmethod
    def joins(Class):
        '''
        List the joins from this fact table to dimension tables.
        yields (column in this table, column in the other table)
        '''
        for column in Class.__table__.columns:
            for foreign_key in column.foreign_keys:
                # foreign_key.target_fullname
                yield column, foreign_key.column

    @classmethod
    def dimensions(Class):
        '''
        List this fact table's dimension tables.
        (tables that this table joins to)
        '''
        for column in Class.__table__.columns:
            for foreign_key in column.foreign_keys:
                yield foreign_key.column.table

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
        Column.__init__(self, *args, **_kwargs)

class Measure(ModelColumn):
    __aggregations__ = []

class ModelTable(Base):

class Dimension(ModelTable):
    '''
    What's info?

    levels are inferred from columns.

    __hierarchies__ is a list of cubes.models.Hierarchy objects
    '''
    __name__ = None
    __hierarchies__ = []

class Fact(ModelTable):
    '''
    Dimensions and joins will be inferred based on foreign keys.
    I think we can do without mappings.
    http://pythonhosted.org/cubes/backends/sql.html#explicit-mapping
    '''
    @classmethod
    def measures(Class):
        '''
        List the measures--not references to dimensions.
        '''
        for column in Class.__table__.columns:
            if len(column.foreign_keys) == 0:
                yield column

    @classmethod
    def joins(Class):
        '''
        List the joins from this fact table to dimension tables.
        This the left element of the tuple is the "dimension"
        in cubes model json language.
        '''
        for column in Class.__table__.columns:
            for foreign_key in column.foreign_keys:
                # foreign_key.target_fullname
                yield column, foreign_key.column

    @classmethod
    def dimensions(Class):
        '''
        List this fact table's dimension tables.
        '''
        for column in Class.__table__.columns:
            for foreign_key in column.foreign_keys:
                yield foreign_key.column.table

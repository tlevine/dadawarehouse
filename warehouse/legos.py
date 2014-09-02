from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import declarative_base as _declarative_base

from cubes.model import Hierarchy, Measure

Base = _declarative_base()

class ModelColumn(_Column):
    'Column in a table, with model metadata'
    def __init__(self, *args, **kwargs):
        _kwargs = dict(kwargs) # copy it rather than mutating it
        if 'label' in _kwargs:
            self.label = _kwargs.pop('label')
        Column.__init__(self, *args, **_kwargs)

class ModelTable(Base):

class Dimension(ModelTable):
    '''
    What's info?
    levels are inferred from columns.
    '''
    name = None
    hierarchies = []

class Fact(ModelTable):
    '''
    Dimensions and joins will be inferred based on foreign keys.
    I think we can do without mappings.
    http://pythonhosted.org/cubes/backends/sql.html#explicit-mapping
    '''
    measures = []
    def joins(self):
        '''
        List the joins from this fact table to dimension tables.
        This the right element of the tuple is the "dimension"
        in cubes model json language.
        '''
        for column in Fact.__table__.columns:
            for foreign_key in column.foreign_keys:
                yield column, foreign_key.column

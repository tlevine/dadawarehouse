from sqlalchemy import Column as _Column
from sqlalchemy.ext.declarative import declarative_base as _declarative_base

from cubes.model import Hierarchy, Measure

Base = _declarative_base()

class ModelColumn(_Column):
    'Column in a table, with model metadata'
    def __init__(self, *args, **kwargs):
        name, label, *rest = args
        self.label = label
        Column.__init__(self, name, *rest, **kwargs)

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

import sqlalchemy as s
from doeund import Fact, Dimension, Column as _Column

def Column(*args, **kwargs):
    'Column with good defaults'
    _kwargs = dict(kwargs)
    if 'nullable' not in _kwargs:
        _kwargs['nullable'] = False
    return _Column(*args, **kwargs) 

def FkColumn(column, *args, **kwargs):
    'Foreign key field'
    return Column(s.Integer, s.ForeignKey(column), *args, **kwargs)

def PkColumn(*args, **kwargs):
    'Primary key field'
    return Column(s.Integer, primary_key = True, *args, **kwargs)

def LabelColumn(*args, **kwargs):
    'A unique string column, for values in a two-column lookup table'
    # Not unique because it works better somewhere
    return Column(s.String, *args, unique = True, **kwargs)

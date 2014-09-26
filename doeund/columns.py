import sqlalchemy as s

class Column(s.Column):
    '''
    Column in a table with good defaults and some model metadata

    This is a normal SQLAlchemy column with two special keyword arguments.

    label: pretty label for the field
    aggregations: list of aggregation functions
    '''
    def __init__(self, *args, **kwargs):
        _kwargs = dict(kwargs) # copy it rather than mutating it
        info = _kwargs.pop('info', {})

        if 'hide' not in info:
            info['hide'] = _kwargs.pop('hide', False)

        if 'label' in _kwargs:
            info['label'] = _kwargs.pop('label')

        if 'nullable' not in _kwargs:
            _kwargs['nullable'] = False

        s.Column.__init__(self, *args, info = info, **_kwargs)

def FkColumn(column, *args, **kwargs):
    'Foreign key field'
    return Column(s.Integer, s.ForeignKey(column), *args, **kwargs)

def PkColumn(*args, **kwargs):
    'Primary key field'
    return Column(s.Integer, primary_key = True, *args, **kwargs)

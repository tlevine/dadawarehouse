import sqlalchemy as s
from doeund import Column as _Column

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
    return Column(s.String, unique = True, *args, **kwargs)

'''
from sqlalchemy import event, DDL
trig_ddl = DDL("""
    CREATE TRIGGER cascade_insert_%(foreign_key_table)s
      AFTER INSERT ON %(foreign_key_table)s
      FOR EACH STATEMENT
      BEGIN
      INSERT IGNORE INTO %(reference_table)s (pk)
        SELECT DISTINCT %(column)s FROM %(foreign_key_table)s;
      END;
""")
tbl = Customer.__table__
event.listen(tbl, 'after_create', trig_ddl.execute_if(dialect='postgresql'))
'''

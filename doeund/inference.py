from collections import OrderedDict
import sqlalchemy.sql.sqltypes as t

def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.
    The implied hierarchy is from left to right along the table.
    '''
    for column in table.columns:
        if not column.primary_key:
            yield {
                'name': column.name,
                'label': column.info.get('label', column.name),
            }

NUMERIC = (
    t.Integer,
    t.Numeric,
    t._DateAffinity,
    t.Boolean,
)

def aggregations(column):
    if isinstance(column, NUMERIC):
        return ['sum', 'avg', 'max']

def fact_measures(table):
    '''
    List the columns that are not foreign keys.
    '''
    return OrderedDict((column.name, [column]) for column in table.columns \
                       if len(column.foreign_keys) == 0)
    for column in table.columns:
        if len(column.foreign_keys) == 0 and column.name != 'pk':
            yield {
                'name': column.name
                'label': column.info.get('label', column.name),
                'aggregations': 
            }

def joins(from_table):
    '''
    List the joins from this fact table to dimension tables.
    '''
    for from_column in from_table.columns:
        for foreign_key in from_column.foreign_keys:
            to_column = foreign_key.column
            to_table = to_column.table
            yield {
                'master': '%s.%s' (from_table.name, from_column.name),
                'detail': '%s.%s' (to_table.name, to_column.name),
            }
            yield from joins(to_table)

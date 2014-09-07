from collections import OrderedDict
import re
from functools import reduce

import sqlalchemy.sql.sqltypes as t

from .columns import nonkey_columns, named_primary_keys, foreign_keys

NUMERIC = (
    t.Integer,
    t.Numeric,
    t._DateAffinity,
    t.Boolean,
)

def named(thingy, contents = {}):
    cube_name = re.sub(r'(?:dim|fact)_', '', thingy.name)
    pretty_name = re.sub(r'[_ ]([a-z])', r' \1',
                      cube_name[0].upper() + cube_name[1:])
    out = dict(contents)
    out.update({
        'name': cube_name,
        'label': thingy.info.get('label', pretty_name),
    })
    return out

def aggregations(column):
    '''
    Choose aggregations based on column type.
    http://cubes.databrewery.org/dev/doc/backends/sql.html?highlight=avg
    '''
    result = ['count', 'count_nonempty', 'count_distinct']
    if isinstance(column, NUMERIC):
        result.extend(['min', 'max', 'avg', 'stddev', 'variance'])
    return result

def fact_measures(table):
    for column in nonkey_columns(table):
        yield named(column, {
            'aggregations': aggregations(column)
        })

def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.
    The implied hierarchy is from left to right along the table.
    '''

    # Normal levels
    for measure in fact_measures(table):
        del(measure['aggregations'])
        yield measure

    # Put primary key last if it appears to be the most precise
    # thing, like for date tables.
    for column in named_primary_keys(table):
        yield named(column)

def joins(table):
    '''
    List the joins from this fact table to dimension tables.
    '''
    for from_table, from_column, to_table, to_column in foreign_keys(table):
        yield {
            'master': '%s.%s' % (from_table.name, from_column.name),
            'detail': '%s.%s' % (to_table.name, to_column.name),
        }
        yield from joins(to_table)

def _stringify_mapping(dimension_path, column):
    '''
    http://cubes.databrewery.org/dev/doc/backends/sql.html?highlight=mappings#explicit-mapping
    '''
    if column.table.name.startswith('dim_'):
        key = '%s.%s' % ('_'.join(dimension_path), column.name)
    elif column.table.name.startswith('fact_'):
        key = column.name
    else:
        raise ValueError('Column %s is neither a dimension nor a fact.' % column.name)

    prefixed_key = prefix + key

    return prefixed_key, '%s.%s' % (column.table.name, column.name)

def _mappings(prefix, table):
    for column in nonkey_columns(table):
        yield prefix, column
    for _, from_column, to_table, to_column in foreign_keys(table):
        if to_table.name.startswith('dim_'):
            dimension_path = [re.sub(r'^dim_', '', column.table.name)]
            yield from _mappings(prefix + dimension_path, to_column.table)

def mappings(table):
    '''
    Produce the mappings dictionary.

    When an attribute corresponds to both a foreign key and its reference,
    report the foreign key column rather than the reference. When a foreign
    key references two different columns, treat them as different dimensions
    and name them reasonably.
    '''
    for dimension, table in _mappings([], table):
        yield _stringify_mapping(dimension, table)

def dimension_names(fact_table):
    result = set()
    for dimension_path, _ in _mappings(fact_table):
        if len(prefix) == 0:
            # This is a measure from the fact table.
            pass
        else:
            result.add('_'.join(dimension))
    return result

def export(tables):
    model = {'dimensions': [], 'cubes': []}
    for table in tables.values():
        if table.name.startswith('fact_'):
            model['cubes'].append(parse_fact(table))
        elif table.name.startswith('dim_'):
            model['dimensions'].append(parse_dimension(table))
    return model

def parse_fact(table):
    return named(table, {
        'dimensions': list(dimension_names(table)),
        'measures': list(fact_measures(table)),
        'joins': list(joins(table)),
        'mappings': dict(mappings(table)),
    })

def parse_dimension(table):
    return named(table, {'levels': list(dim_levels(table))})


# Here's a problem: If the same dimension table is used for two different
# dimensions in a cube (like multiple different dates), it only gets shown
# once. Also, the name is unclear because it uses the dimension table name
# rather than the fact table name.

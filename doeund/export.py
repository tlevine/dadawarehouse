from collections import OrderedDict
import re
from functools import reduce

import sqlalchemy.sql.sqltypes as t

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
    '''
    List the columns that are not foreign keys.
    '''
    for column in table.columns:
        if not column.primary_key and len(column.foreign_keys) == 0:
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
    for column in table.columns:
        if column.primary_key and column.name != 'pk':
            yield named(column)

def joins(from_table):
    '''
    List the joins from this fact table to dimension tables.
    '''
    for from_column in from_table.columns:
        for foreign_key in from_column.foreign_keys:
            to_column = foreign_key.column
            to_table = to_column.table
            yield {
                'master': '%s.%s' % (from_table.name, from_column.name),
                'detail': '%s.%s' % (to_table.name, to_column.name),
            }
            yield from joins(to_table)

def _mapping(column):
    '''
    http://cubes.databrewery.org/dev/doc/backends/sql.html?highlight=mappings#explicit-mapping
    '''
    if column.table.name.startswith('dim_'):
        dimension = re.sub(r'^dim_', '', column.table.name)
        attribute = column.name
        key = '%s.%s' % (dimension, attribute)
    elif column.table.name.startswith('fact_'):
        key = column.name
    else:
        raise ValueError('Column %s is neither a dimension nor a fact.' % column.name)

    return key, '%s.%s' % (column.table.name, column.name)

def mappings(table):
    for column in table.columns:
        yield _mapping(column)
        for foreign_key in column.foreign_keys:
            if not column.primary_key and len(column.foreign_keys) == 0:
                yield from mappings(foreign_key.column.table)

def dimension_names(fact_table):
    result = set()
    for key, value in mappings(fact_table):
        if key.count('.') == 1:
            # Fact attributes have zero dots,
            # and dimension attributes have one dot.
            dimension, attribute = key.split('.')
            result.add(dimension)
    return result

def export(tables):
    model = {'dimensions': [], 'cubes': []}
    previous_dimensions = set()
    for table in tables.values():
        if table.name.startswith('fact_'):
            model['cubes'].append(parse_fact(table))
            for dimension in parse_dimensions(table):
                if dimension['name'] not in previous_dimensions:
                    model['dimensions'].append(dimension)
                    previous_dimensions.add(dimension['name'])
    return model

def parse_fact(table):
    return named(table, {
        'dimensions': list(dimension_names(table)),
        'measures': list(fact_measures(table)),
        'joins': list(joins(table)),
        'mappings': dict(mappings(table)),
    })

def parse_dimensions(table):
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            levels = list(dim_levels(foreign_key.column.table))
            yield named(column, {'levels': levels})
            yield from parse_dimensions(foreign_key.column.table)

from collections import OrderedDict, namedtuple
import re
from functools import reduce, partial

import sqlalchemy.sql.sqltypes as t

from .columns import nonkey_columns, named_primary_keys, foreign_keys, \
                     is_crosswalk

class DimensionPath(list):
    '''
    A list of table names that specifies a joined dimension
    '''
    info = {}
    @property
    def name(self):
        if len(self) > 0:
            return '_'.join(map(partial(re.sub, r'^(?:dim|fact)_', ''), self))

def named(thingy, contents = {}):
    name = re.sub(r'(?:dim|fact)_', '', thingy.name)
    label = (word[0].upper() + word[1:] for word in re.split(r'[ _]', name))
    out = dict(contents)
    out.update({
        'name': name,
        'label': thingy.info.get('label', ' '.join(label)),
    })
    return out

NUMERIC = (
    t.Integer,
    t.Numeric,
    t._DateAffinity,
    t.Boolean,
)

def aggregates(column):
    '''
    Choose aggregations based on column type.
    http://cubes.databrewery.org/dev/doc/backends/sql.html?highlight=avg
    '''
    result = ['count', 'count_nonempty', 'count_distinct']
    if isinstance(column, NUMERIC):
        result.extend(['min', 'max', 'avg', 'stddev', 'variance', 'sum'])
    return result

def fact_measures(table):
    for column in nonkey_columns(table):
        yield named(column, {
            'aggregates': aggregates(column)
        })

def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.
    The implied hierarchy is from left to right along the table.
    '''

    # Normal levels
    for measure in fact_measures(table):
        del(measure['aggregates'])
        yield measure

    # Put primary key last if it appears to be the most precise
    # thing, like for date tables.
    for column in named_primary_keys(table):
        yield named(column)

def joins(table, prefix = None):
    '''
    List the joins from this fact table to dimension tables.
    '''
    if prefix == None:
        # table is a fact table
        prefix = [table.name]
    for from_table, from_column, to_table, to_column in foreign_keys(table):
        if is_crosswalk(to_table):
            suffix = []
        else:
            suffix = [to_table.name]
        path = DimensionPath(prefix + suffix)
        alias = 'dim_' + path.name
        yield {
            'master': '%s.%s' % (from_table.name, from_column.name),
            'detail': '%s.%s' % (to_table.name, to_column.name),
            'alias': alias,
        }
        yield from joins(to_table, prefix = path)

def _stringify_mapping(dimension_path, column):
    '''
    http://cubes.databrewery.org/dev/doc/backends/sql.html?highlight=mappings#explicit-mapping
    '''
    if len(dimension_path) == 1:
        key = column.name
    else:
        key = '%s.%s' % (dimension_path.name, column.name)

    return key, '%s.%s' % (column.table.name, column.name)

def _mappings(prefix, table):
    for column in nonkey_columns(table):
        yield prefix, column
    for _, from_column, to_table, to_column in foreign_keys(table):
        if to_table.name.startswith('dim_'):
            if is_crosswalk(to_table):
                suffix = []
            else:
                suffix = [to_table.name]
            path = DimensionPath(prefix + suffix)
            yield from _mappings(path, to_column.table)

def mappings(table):
    '''
    Produce the mappings dictionary.

    When an attribute corresponds to both a foreign key and its reference,
    report the foreign key column rather than the reference. When a foreign
    key references two different columns, treat them as different dimensions
    and name them reasonably.
    '''
    for dimension, table in _mappings(DimensionPath([table.name]), table):
        yield _stringify_mapping(dimension, table)

def dimensions(fact_table):
    result = set()
    for dimension, column in _mappings(DimensionPath([fact_table.name]), fact_table):
        if len(dimension) == 0:
            raise AssertionError('This shouldn\'t happen.')
        elif len(dimension) == 1:
            # This is a measure from the fact table.
            pass
        elif dimension.name not in result:
            result.add(dimension.name)
            yield dimension

def export(tables):
    result = set()
    model = {'dimensions': [], 'cubes': []}
    for table in tables.values():
        if table.name.startswith('fact_'):
            model['cubes'].append(parse_fact(table))
            for dimension in dimensions(table):
                d = named(dimension, {'levels': list(dim_levels(table))})
                model['dimensions'].append(d)
    return model

def parse_fact(table):
    return named(table, {
        'dimensions': [d.name for d in dimensions(table)],
        'measures': list(fact_measures(table)),
        'joins': list(joins(table)),
        'mappings': dict(mappings(table)),
    })


# Here's a problem: If the same dimension table is used for two different
# dimensions in a cube (like multiple different dates), it only gets shown
# once. Also, the name is unclear because it uses the dimension table name
# rather than the fact table name.

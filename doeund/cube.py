'''
Group the fact table's columns into two categories

References
    Foreign keys that reference dimensions
Measures
    Not foreign keys, which are each dimensions themselves

(The primary key will fall into one of these categories.)

Group each dimension's columns into three categories.

Primary keys
    Primary keys on this table
Foreign keys
    References to another dimension table
Levels
    Everything else

Treat the levels as components of the dimension.
'''
import functools

class Cube:
    dimensions = {}
    # A dictionary of string keys and list-of-Column-object values,
    # traversing recursively into the full snowflake of dimensions

    def __init__(self, session, fact_table):
        '''
        fact_table: a Fact class
        '''
        # Flatten the table, and record dimensions
        self.dimensions.update(fact_measures(fact_table))
        self.query = session.query(fact_table)
        tables = [fact_table]
        while len(tables) > 0:
            for from_column, to_column, to_table in fact_joins(tables.pop()):
                self.query = self.query.join(to_table, from_column == to_column)
                self.dimensions[to_table.name] = dim_levels(to_table)
                tables.push(to_table)

    def point_cut(self, dimension, path):
        # Copy the query
        query = self.query.all()

        # Drill down as deep as the path allows.
        for level, value in zip(self.dimensions[dimension], path):
            query = self.query.filter(level == value)
        return query

    def set_cut(self, dimension, paths):
        subqueries = map(functools.partial(self.point_cut, dimension), paths)
        if len(subqueries) >= 1:
            q, *qs = subqueries
        return q.union_all(qs)

    def range_cut(self, dimension, from_path, to_path):
        'from_path must be less than to_path'
        # Copy the query
        query = self.query.all()

        # Drill down as deep as the path allows.
        for level, value in zip(self.dimensions[dimension], from_path):
            query = self.query.filter(level >= value)
        for level, value in zip(self.dimensions[dimension], to_path):
            query = self.query.filter(level <= value)

        return query

def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.
    The implied hierarchy is from left to right along the table.
    '''
    return [column for column in table.columns if not column.primary_key]

def fact_measures(table):
    '''
    List the columns that are not foreign keys.
    '''
    return {column.name: [column] for column in table.columns \
            if not len(column.foreign_keys) == 0}

def joins(table):
    '''
    List the joins from this fact table to dimension tables.
    yields (column in this table, column in the other table)
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            yield column, foreign_key.column, foreign_key.column.table

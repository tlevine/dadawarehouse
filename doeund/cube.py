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

class Cube:
    def __init__(self, fact_table):
        '''
        fact_table: a Fact class
        '''
        self.fact = fact_table

        # A dictionary of string keys and Column object values,
        # traversing recursively into the full snowflake of dimensions
        self.dimensions

    def point_cut(self, dimension, path):
        raise NotImplementedError

    def set_cut(self, dimension, paths):
        raise NotImplementedError

    def range_cut(self, dimension, from_path, to_path):
        raise NotImplementedError
    


def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.
    The implied hierarchy is from left to right along the table.
    '''
    return filter(lambda column: not column.primary_key, table.columns)

def fact_measures(table):
    '''
    List the columns that are not foreign keys.
    '''
    return filter(lambda column: len(column.foreign_keys) == 0, table.columns)

def fact_joins(table):
    '''
    List the joins from this fact table to dimension tables.
    yields (column in this table, column in the other table)
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            # foreign_key.target_fullname
            yield column, foreign_key.column

def fact_dimensions(table):
    '''
    List this fact table's dimension tables.
    (tables that this table joins to)
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            yield foreign_key.column.table

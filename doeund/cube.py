def cube(table):
    '''
    table:: a Fact table
    '''

    


def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.'
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

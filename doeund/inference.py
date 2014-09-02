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

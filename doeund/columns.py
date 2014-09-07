def nonkey_columns(table):
    '''
    Columns in the present table that are not foreign keys.
    '''
    for column in table.columns:
        if not column.primary_key and len(column.foreign_keys) == 0:
            yield column

def named_primary_keys(table):
    '''
    Columns in the present table that primary keys with names other than "pk".
    '''
    for column in table.columns:
        if column.primary_key and column.name != 'pk':
            yield column

def foreign_key_references(table):
    '''
    Columns (usually from other tables) that are referenced by this table's
    foreign keys
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys
            yield foreign_key.column

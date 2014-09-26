from sqlalchemy.sql.schema import ForeignKeyConstraint

def joins(table):
    '''
    List the joins from this fact table to dimension tables.
    '''
    for from_table, from_columns, to_table, to_columns in foreign_keys(table):
        yield [(
                '%s.%s' % (from_table, from_column),
                '%s.%s' % (to_table, to_column),
        ) for from_column, to_column in zip(from_columns, to_columns)]
        yield from joins(to_table)

def foreign_keys(table):
    '''
    Columns (usually from other tables) that are referenced by this table's
    foreign keys
    '''
    for constraint in table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):
            for foreign_key in column.foreign_keys:
                from_table = table.name
                from_columns = [col.name for col in foreign_key.columns]

                to_table = foreign_key.column.table.name
                to_columns = [fk.column.name for fk in foreign_key.elements]

                yield from_table, from_columns, to_table, to_columns

import re

from sqlalchemy.sql.schema import ForeignKeyConstraint

from doeund.templates import drop_view, create_view

def make_cubes(tables):
    for table in tables.values():
        if table.name.startswith('ft_'):
            fact_table_base = re.sub(r'^ft_', '', table.name)
            yield drop_view.substitute(fact_table_base = fact_table_base)
            yield create_view.substitute(fact_table_base = fact_table_base,
                                         joins = list(joins(table)))

def joins(table):
    '''
    List the joins from this fact table to dimension tables.
    '''
    for from_table, from_columns, to_table, to_columns in foreign_keys(table):
        yield (to_table.name, [(
                '%s.%s' % (from_table.name, from_column.name),
                '%s.%s' % (to_table.name, to_column.name),
        ) for from_column, to_column in zip(from_columns, to_columns)])
#       yield from joins(to_table)

def foreign_keys(table):
    '''
    Columns (usually from other tables) that are referenced by this table's
    foreign keys
    '''
    for constraint in table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):
            from_table = table
            from_columns = [col for col in constraint.columns]

            to_table = constraint.table
            to_columns = [fk.column for fk in constraint.elements]

            yield from_table, from_columns, to_table, to_columns

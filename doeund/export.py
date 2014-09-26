import re
import itertools

from sqlalchemy.sql.schema import ForeignKeyConstraint

from doeund.templates import drop_view, create_view

def make_cubes(tables):
    for table in tables.values():
        if table.name.startswith('ft_'):
            fact_table_base = re.sub(r'^ft_', '', table.name)
            yield drop_view.substitute(fact_table_base = fact_table_base)
            yield create_view.substitute(
                fact_table_base = fact_table_base,
                columns = list(columns_to_select(table)),
                joins = list(joins(table)))

def aliased_column_name(column):
    alias = '%s_%s' % (re.sub(r'^(?:ft_|dim_)', '', column.table.name), column.name)
    return '"%s"."%s" AS "%s"' % (table.name, column.name, alias)

def unaliased_column_name(column):
    return '"%s"."%s"' % (column.table.name, column.name)

def columns_to_select(table, aliased = False):
    '''
    Come up with a list of columns to put in the select statement.
    '''
    from_table = table
    do_not_select = set()
    for on_columns in joins(table):
        for from_column, _ in on_columns:
            do_not_select.add(from_column.table.name, from_column.name)
        yield from columns_to_select(to_table, aliased = True)

    for column in table.columns:
        f = aliased_column_name if aliased else unaliased_column_name
        if (column.table.name, column.name) not in do_not_select and not column.info['hide']:
            yield f(column)

def joins(table):
    '''
    List the joins from this table.

    This automatically detects joins that are encoded as
    foreign keys. If you have joins that are not encoded as
    foreign keys, use the add_join class method.
    '''
    yield from table.info.get('joins', [])
    for from_table, from_columns, to_table, to_columns in foreign_keys(table):
        yield [(from_column,to_column) \
               for from_column, to_column in zip(from_columns, to_columns)]
        yield from joins(to_table)

def join_strings(table):
    for on_columns in joins(table):
        for from_column, to_column in on_columns:
            yield (on_columns[0].table.name, [(
                unaliased_column_name(from_column),
                unaliased_column_name(to_column),
            ) for from_column, to_column in on_columns])


def foreign_keys(table):
    '''
    Columns (usually from other tables) that are referenced by this table's
    foreign keys
    '''
    for constraint in table.constraints:
        if isinstance(constraint, ForeignKeyConstraint):
            from_columns = [col for col in constraint.columns]
            from_table = constraint.table

            to_columns = [fk.column for fk in constraint.elements]
            if len(set(to_column.table.name for to_column in to_columns)) != 1:
                raise AssertionError('This shouldn\'t happen.')
            to_table = to_columns[0].table

            yield from_table, from_columns, to_table, to_columns

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

def full_column_name(table_name, column_name):
    alias = '%s_%s' % (table_name, column_name)
    return '"%s"."%s" AS "%s"' % (table_name, column_name, alias)

def columns_to_select(table):
    '''
    Come up with a list of columns to put in the select statement.
    '''
    do_not_select = set()
    for from_table, from_columns, to_table, _ in foreign_keys(table):
        for from_column in from_columns:
            do_not_select.add(full_column_name(from_table.name, from_column.name))
        yield from columns_to_select(to_table)

    for column in table.columns:
        name = full_column_name(table.name, column.name)
        if name not in do_not_select and not column.info['hide']:
            yield name

def joins(table):
    '''
    List the joins from this fact table to dimension tables
    in the following format. ::

        [('to table', [('[from table].[from column]',
                        '[to table].[to column]'),
                       ('[from table].[from column]',
                        '[to table].[to column]'),
                       ...]),
         ('to table', [('[from table].[from column]',
                        '[to table].[to column]'),
                       ('[from table].[from column]',
                        '[to table].[to column]'),
                       ...]),
         ...]

    This automatically detects joins that are encoded as
    foreign keys. If you have joins that are not encoded as
    foreign keys, set the ``__joins__`` class attribute
    with the add_join class method.

        Foo.__joins__ = [('dim_emailaddress',
            ('email_address', 'local_id')]

    This is the same format as above but without the
    "from table" and "to table" from the list in the right
    of the tuple.
    '''
    yield from getattr(table, '__joins__', [])
    for from_table, from_columns, to_table, to_columns in foreign_keys(table):
        yield (to_table.name, [(
                '"%s"."%s"' % (from_table.name, from_column.name),
                '"%s"."%s"' % (to_table.name, to_column.name),
        ) for from_column, to_column in zip(from_columns, to_columns)])
        yield from joins(to_table)

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

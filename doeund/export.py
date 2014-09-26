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

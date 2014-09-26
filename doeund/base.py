from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

Base = _declarative_base()

class DadaBase(Base):
    __abstract__ = True
    def __joins__(Class):
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

        Override this if you have joins that are not specified in
        the foreign keys.
        '''
        table = Class.__table__
        for from_table, from_columns, to_table, to_columns in foreign_keys(table):
            yield (to_table.name, [(
                    '%s.%s' % (from_table.name, from_column.name),
                    '%s.%s' % (to_table.name, to_column.name),
            ) for from_column, to_column in zip(from_columns, to_columns)])
            yield from joins(to_table)

class Fact(DadaBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'ft_' + Class.__name__.lower()

class Dimension(DadaBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'dim_' + Class.__name__.lower()

class Helper(DadaBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(Class):
        return 'helper_' + Class.__name__.lower()

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


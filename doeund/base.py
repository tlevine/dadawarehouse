from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

Base = _declarative_base()

class DadaBase(Base):
    __abstract__ = True
    __joins__ = []

    @classmethod
    def add_join(Class, to_table_name, on_columns):
        from_table = Class.__table__
        the_join = (to_table_name, [(
            '%s.%s' % (from_table.name, from_column_name),
            '%s.%s' % (to_table_name, to_column_name),
        ) for from_column_name, to_column_name in on_columns])
        Class.__table__.__joins__.append(the_join)

    @classmethod
    def joins(Class):
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
        yield from table.__joins__
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


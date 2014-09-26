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
        if not hasattr(Class.__table__, '__joins__'):
            Class.__table__.__joins__ = []
        Class.__table__.__joins__.append(the_join)

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

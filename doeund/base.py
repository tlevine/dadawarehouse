from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

Base = _declarative_base()

class DadaBase(Base):
    __abstract__ = True

    @classmethod
    def add_join(from_class, on_columns):
        from_table = from_class.__table__
        
        if 'joins' not in from_table.info:
            from_table.info['joins'] = []

        from_table.info['joins'].append(
            (to_table, [(
                (from_table, from_column),
                (to_table, to_column),
            ) for from_column, to_column in on_columns]))

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

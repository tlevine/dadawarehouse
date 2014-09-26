from sqlalchemy.ext.declarative import \
    declarative_base as _declarative_base, declared_attr

Base = _declarative_base()

class DadaBase(Base):
    __abstract__ = True
    __joins__ = []

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

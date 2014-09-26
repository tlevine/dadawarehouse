import sqlalchemy as s

from doeund import Fact, Column

class MuttAlias(Fact):
    pk = Column(s.String, primary_key = True)
    name = Column(s.String, nullable = True)
    email_address = Column(s.String)

import sqlalchemy as s
from sqlalchemy.dialects.postgres import CIDR
from sqlalchemy.orm import relationship

from doeund import Fact, PkColumn, Column

class BranchableLog(Fact):
    pk = PkColumn()
    route = Column(s.String)
    status_code = Column(s.Integer)
    ip_address = Column(CIDR)
    datetime = Column(s.DateTime)
    user_agent = Column(s.String)


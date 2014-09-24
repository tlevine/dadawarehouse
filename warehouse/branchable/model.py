import sqlalchemy as s

from ..model import Fact, PkColumn, Column

class BranchableLog(Fact):
    pk = PkColumn()
    route = Column(s.String)
    status_code = Column(s.Integer)
    ip_address = Column(s.String)
    datetime = Column(s.DateTime)
    user_agent = Column(s.String)

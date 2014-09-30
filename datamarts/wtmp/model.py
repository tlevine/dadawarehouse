from doeund import Fact, Column

import sqlalchemy as s
from sqlalchemy.dialects.postgres import CIDR

Computer = s.Enum('laptop', 'home', 'nsa', name = 'computer_name')

class Last(Fact):
    computer = Column(Computer, primary_key = True)
    filename = Column(s.String)
    user = Column(s.String)
    ip_address = Column(CIDR)
    login_datetime = Column(s.DateTime)
    logout_datetime = Column(s.DateTime)

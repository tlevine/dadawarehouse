from doeund import Fact, Column

import sqlalchemy as s
from sqlalchemy.dialects.postgres import CIDR

from .parse import parse

Computer = s.Enum('laptop', 'home', 'nsa', name = 'computer_name')

class Last(Fact):
    computer = Column(Computer, primary_key = True)
    filename = Column(s.String)
    user = Column(s.String)
    ip_address = Column(CIDR)
    login_datetime = Column(s.DateTime)
    logout_datetime = Column(s.DateTime, nullable = True)

    @classmethod
    def factory(Class, computer, filename, line):
        kwargs = {
            'computer': computer,
            'filename': filename,
        }
        kwargs.update(parse(line))
        return Class(**kwargs)

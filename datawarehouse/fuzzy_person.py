import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgres import CIDR

from doeund import Fact, Column, PkColumn
from datamarts import (
    BranchableLog,
)
from .person import GidColumn, Person

class Name(Fact):
    pk = PkColumn(hide = True)
    global_id = GidColumn()
    person = relationship(Person)
    local_id = Column(s.String)

class IPAddress(Fact):
    pk = PkColumn(hide = True)
    global_id = GidColumn()
    person = relationship(Person)
    local_id = Column(CIDR)

class PiwikVisitorId(Fact):
    pk = PkColumn(hide = True)
    global_id = GidColumn()
    person = relationship(Person)
    local_id = Column(s.String)

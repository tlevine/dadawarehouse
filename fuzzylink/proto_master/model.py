import sqlalchemy as s

from doeund import Base

class ProtoMaster(Base):
    '''
    A place to store the guesses of what the master data might be
    '''
    __tablename__ = 'proto_master'
    pk = PkColumn()
    context = Column(s.String)
    global_id = Column(s.String)
    local_id = Column(s.String)

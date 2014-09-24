from .model import Base
from .mutt_aliases import mutt_aliases

def load(warehouse_session, master_engine):
    Base.metadata.create_all(master_engine) 
    master_session = sessionmaker(bind=master_engine)()
    master_session.add_all(mutt_aliases())

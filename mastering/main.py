from sqlalchemy.orm import sessionmaker

from .piwik_email.load import piwik_email
from .piwik_email.model import PiwikEmailOverlap

def load(engine):
    sm = sessionmaker(bind=engine)
    piwik_email(sm)

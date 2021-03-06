import os
import csv
from collections import Counter

from sqlalchemy.ext.declarative import declarative_base

from datamarts.logger import logger
from datamarts import (
    BranchableLog,
    FacebookNameChange,
    MuttAlias,
    NotmuchMessage,
    PiwikVisitorLocation,
    TwitterAction,
)

from .model import (
    Person,
    PersonEmailAddress, PersonFacebook, PersonTwitter,
    PersonName, PersonLocation, PiwikVisitor,
)

def load_piwik(session):
    old = set(r[0] for r in session.query(PiwikVisitor.id).distinct())
    new = set(r[0] for r in session.query(PiwikVisitorLocation.visitor_id).distinct())
    session.add_all(PiwikVisitor(id = visitor_id) for visitor_id in (new - old))
    session.flush()

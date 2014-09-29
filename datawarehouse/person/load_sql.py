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
    EmailAddress, Facebook, Twitter,
    PersonName, PersonLocation, PiwikVisitor,
)

def load_piwik(session):
    query = session.query(PiwikVisitorLocation.visitor_id).distinct()
    session.add_all(PiwikVisitor(id = row[0]) for row in query)
    session.flush()

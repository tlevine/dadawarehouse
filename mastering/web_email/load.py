from collections import defaultdict

import sqlalchemy as s

from datamarts import NotmuchMessage, PiwikVisit

from .model import PiwikEmailOverlap

def piwik_email(sessionmaker):
    session = sessionmaker()



    query = session.query(s.func.date(BranchableLog.datetime),
                          BranchableLog.ip_address).distinct()\
                   .union(
                                      PiwikVisit.serverDateTime,
                                      PiwikVisit.visitIp)
    ip_address_days = identifier_sets(query)

    query = session.query(NotmuchMessage.datetime,
                          NotmuchMessage.from_address).distinct()
    email_address_days = identifier_sets(query)

    query = session.query(PiwikVisit.serverDateTime,
                          PiwikVisit.visitorId).distinct()
    piwik_visitorid_days = identifier_sets(query)

    session.query(PiwikEmailOverlap).delete()
    session.flush()
    session.add_all(pairwise_check(email_address_days,
                                   piwik_visitorid_days))
    session.commit()

def pairwise_check(email_address_days, piwik_visitorid_days):
    for email_address, email_dates in email_address_days.items():
        for piwik_visitorid, piwik_dates in piwik_visitorid_days.items():
            intersection = len(email_dates.intersection(piwik_dates))
            union = len(email_dates.union(piwik_dates))
            yield PiwikEmailOverlap(email_address = email_address,
                                    visitor_id = piwik_visitorid,
                                    intersecting_dates = intersection,
                                    unioned_dates = union)

def identifier_sets(query):
    identifier_days = defaultdict(set)
    for date, identifier, count in query:
        if count >= 2:
            identifier_days[identifier].add(date)
    return identifier_days

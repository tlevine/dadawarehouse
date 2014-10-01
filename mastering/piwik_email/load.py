from collections import defaultdict

def piwik_email(sessionmaker):
    session = sessionmaker()

    email_address_days = identifier_sets(session,
                                         NotmuchMessage.datetime,
                                         NotmuchMessage.email_address)
    piwik_visitorid_days = identifier_sets(session,
                                           PiwikVisit.serverDateTime,
                                           PiwikVisit.visitorId)

    session.query(PiwikEmailOverlap).delete()
    session.flush()
    session.add_all(pairwise_check(email_address_days,
                                   piwik_visitorid_days))
    session.commit()

def pairwise_check(email_address_days, piwik_visitorid_days):
    for email_address, email_dates in email_address_days:
        for piwik_visitorid, piwik_dates in piwik_visitorid_days:
            intersection = len(email_dates.intersection(piwik_dates))
            union = len(email_dates.union(piwik_dates))
            yield PiwikEmailOverlap(email_address = email_address,
                                    piwik_visitorid = piwik_visitorid,
                                    intersecting_dates = intersection,
                                    unioned_dates = union)

def identifier_sets(session, datetime_column, identifier_column)
    identifier_days = defaultdict(set)
    query = session.query(s.func.date(datetime_column), identifier_column)
                   .group_by(s.func.date(datetime_column), identifier_column)
                   .filter(s.func.count(identifier_column) >= 2)
    for date, identifier in query:
        identifier_days[identifier].add(date)
    return identifier_days

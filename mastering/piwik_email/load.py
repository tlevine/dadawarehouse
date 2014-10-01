from collections import defaultdict

def piwik_email(sessionmaker):
    email_address_days = identifier_sets(sessionmaker(),
                                         EmailAddressDays.date,
                                         EmailAddressDays.email_address)
    piwik_visitorid_days = identifier_sets(sessionmaker(),
                                           PiwikVisitorDays.date,
                                           PiwikVisitorDays.visitor_id)

    session = sessionmaker()
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

def identifier_sets(session, date_column, identifier_column)
    identifier_days = defaultdict(set)
    query = session.query(date_column, identifier_column)
    for date, identifier in query:
        identifier_days[identifier].add(date)
    for identifier, days in identifier_days.items():
        if len(days) <= 2:
            del(identifier_days[identifier])
    return identifier_days

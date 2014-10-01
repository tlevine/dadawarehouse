from collections import defaultdict

def piwik_email(sessionmaker):
    session = sessionmaker()

    email_address_days = identifier_sets(sessionmaker(),
                                         EmailAddressDays.date,
                                         EmailAddressDays.email_address)
    piwik_visitorid_days = identifier_sets(sessionmaker(),
                                           PiwikVisitorDays.date,
                                           PiwikVisitorDays.visitor_id)

    for email_address, email_dates in email_address_days:
        for piwik_visitorid, piwik_dates in piwik_visitorid_days:
            intersection = len(email_dates.intersection(piwik_dates))
            union = len(email_dates.union(piwik_dates))
            intersection / union

def identifier_sets(session, date_column, identifier_column)
    identifier_days = defaultdict(set)
    query = session.query(date_column, identifier_column)
    for date, identifier in query:
        identifier_days[identifier].add(date)
    return identifier_days

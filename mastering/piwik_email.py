from collections import defaultdict

def piwik_email(sessionmaker):
    session = sessionmaker()

    email_address_days = identifier_sets(sessionmaker(),
                                         EmailAddressDays.date,
                                         EmailAddressDays.email_address)
    piwik_visitorid_days = identifier_sets(sessionmaker(),
                                           PiwikVisitorDays.date,
                                           PiwikVisitorDays.visitor_id)

def identifier_sets(session, date_column, identifier_column)
    identifier_days = defaultdict(set)
    query = session.query(date_column, identifier_column)
    for date, identifier in query:
        identifier_days[identifier].add(date)
    return identifier_days

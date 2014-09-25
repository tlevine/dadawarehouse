import os
import datetime

from lxml.etree import fromstring
import requests

def update(session):
    key = 'PIWIK_API_TOKEN'
    if key not in os.environ:
        raise ValueError('You need to set the %s environment variable.' % key)

    # The most recent date
    date = session.query(PiwikVisit.date).order_by(desc(PiwikVisit.date)).scalar()

    # Delete things from the most recent date in case of partial dates.
    session.query(PiwikVisit).filter(PiwikVisit.date == date).delete()
    session.commit()

    while date <= datetime.date.today():
        response = get_visits(os.environ[key], date)
        session.add_all(parse_visits(response))
        session.commit()
        date += date + datetime.timedelta(days = 1)

def visits(token, date):
    for offset in itertools.count(0, 100):
        response = get_visits(token, date, offset)
        visits = map(reify_visit, json.loads(response.text))
        yield from visits
        if len(visits) == 0:
            break

def get_visits(token, date, page): 
    url = 'http://piwik.thomaslevine.com'
    params = {
        'module': 'API',
        'method': 'Live.getLastVisitsDetails',
        'idSite': '2',
        'period': 'day',
        'date': date.isoformat(),
        'format': 'xml',
        'token_auth': token,
        'filter_limit': 100,
        'filter_offset': offset,
    }
    return requests.get(url, params = params)

def reify_visit(blob):
    pass

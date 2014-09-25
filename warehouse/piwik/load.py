import os
import itertools
import json
import datetime

import requests
from sqlalchemy import desc

from .model import PiwikAction, PiwikVisit

def update(session):
    key = 'PIWIK_API_TOKEN'
    if key not in os.environ:
        raise ValueError('You need to set the %s environment variable.' % key)

    # The most recent date
    most_recent = session.query(PiwikVisit.serverDateTime)\
                         .order_by(desc(PiwikVisit.serverDateTime))\
                         .scalar()
    if most_recent == None:
        date = oldest_visit(os.environ[key]).date()

    else:
        # Delete things from the most recent _datetime in case of partial dates.
        _datetime = datetime.datetime.combine(most_recent.date(), datetime.time())
        date = most_recent.date()

        session.query(PiwikVisit)\
               .filter(PiwikVisit.serverDateTime >= _datetime)\
               .delete()
        session.query(Action).filter(Action.datetime >= _datetime).delete()
        session.commit()

    while date <= datetime.date.today():
        session.add_all(visits(os.environ[key], date))
        session.commit()
        date += date + datetime.timedelta(days = 1)
        logger.info('Loaded visits for %s' % date.isoformat())

def visits(token, date):
    for offset in itertools.count(0, 100):
        response = get_visits(token, date, offset)
        rawvisits = json.loads(response.text)
        yield from itertools.chain(*map(reify_visit, rawvisits))
        if len(rawvisits) == 0:
            break

def oldest_visit(token):
    url = 'http://piwik.thomaslevine.com'
    params = {
        'module': 'API',
        'method': 'Live.getLastVisitsDetails',
        'idSite': '2',
        'period': 'range',
        'year': '2000,2020',
        'format': 'json',
        'token_auth': token,
        'filter_limit': 1,
        'filter_sort_order': 'asc',
        'showColumns': 'serverDate',
    }
    response = requests.get(url, params = params)
    rawdate = json.loads(response.text)[0]['serverDate']
    return datetime.datetime.strptime(rawdate, '%Y-%m-%d')

def get_visits(token, date, offset): 
    url = 'http://piwik.thomaslevine.com'
    params = {
        'module': 'API',
        'method': 'Live.getLastVisitsDetails',
        'idSite': '2',
        'period': 'day',
        'date': date.isoformat(),
        'format': 'json',
        'token_auth': token,
        'filter_limit': 100,
        'filter_offset': offset,
    }
    return requests.get(url, params = params)

def reify_visit(v):
    screen_width, screen_height = tuple(map(int, v['resolution'].split('x')))
    visit = PiwikVisit(
        idVisit = int(v['idVisit']),
        serverDateTime = datetime.datetime.fromtimestamp(v['serverTimestamp']),
        clientTime = datetime.time(*map(int, v['visitLocalTime'].split(':'))),

        actions = int(v['actions']),
        browserCode = v['browserCode'],
        browserFamily = v['browserFamily'],
        browserFamilyDescription = v['browserFamilyDescription'],
        browserName = v['browserName'],
        browserVersion = v['browserVersion'],

        city = v['city'],
        continent = v['continent'],
        continentCode = v['continentCode'],
        country = v['country'],
        countryCode = v['countryCode'],
        
        daysSinceFirstVisit = int(v['daysSinceFirstVisit']),
        daysSinceLastVisit = int(v['daysSinceLastVisit']),
        
        deviceType = v['deviceType'],
        events = int(v['events']),
        
        idSite = int(v['idSite']),
        firstActionDate = datetime.datetime.fromtimestamp(v['firstActionTimestamp']),
        lastActionDate = datetime.datetime.fromtimestamp(v['lastActionTimestamp']),
        
        location = v['location'],
        latitude = float(v['latitude']),
        longitude = float(v['longitude']),
        
        operatingSystem = v['operatingSystem'],
        operatingSystemCode = v['operatingSystemCode'],
        operatingSystemShortName = v['operatingSystemShortName'],
        
    #   plugins = 'pdf, flash, java, quicktime',
        
        provider = v['provider'],
        providerName = v['providerName'],
        providerUrl = v['providerUrl'],
        referrerKeyword = v['referrerKeyword'],
        referrerKeywordPosition = v['referrerKeywordPosition'],
        referrerName = v['referrerName'],
        referrerSearchEngineUrl = v['referrerSearchEngineUrl'],
        referrerType = v['referrerType'],
        referrerTypeName = v['referrerTypeName'],
        referrerUrl = v['referrerUrl'],
        region = v['region'],
        regionCode = v['regionCode'],
        
        screen_width = screen_width,
        screen_height = screen_height,
        screenType = v['screenType'],
        searches = int(v['searches']),
        visitCount = int(v['visitCount']),
        visitDuration = int(v['visitDuration']),
        visitIp = v['visitIp'],
        visitorId = v['visitorId'],
        visitorType = v['visitorType'],
    )
    yield visit
    for action in v['actionDetails']:
        time = datetime.time(*map(int, action['serverTimePretty'].split(' ')[-1].split(':')))
        _datetime = datetime.datetime.combine(visit.serverDateTime.date(), time)
        yield PiwikAction(
            visit_id = int(v['idVisit']),

            page_id = int(action['pageId']),
            page_id_action = None if action['pageIdAction'] == None else int(action['pageIdAction']),

            page_title = action['pageTitle'],
            action_type = action['actionType'],
            datetime = _datetime,
            url = action['url'],
        )

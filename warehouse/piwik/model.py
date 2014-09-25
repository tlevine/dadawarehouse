import sqlalchemy as s

import warehouse.model as m

class Action(m.Fact):
    visit_id = m.Column(s.Integer, s.ForeignKey(Visit), primary_key = True)
    action_id = m.Column(s.Integer, primary_key = True)

    page_id = m.Column(s.Integer)
    page_id_action = m.Column(s.Integer)
    page_title = m.Column(s.String)
    server_time = m.Column(s.DateTime)
    action_type = m.Column(s.String)
    url = m.Column(s.String)

class Visit(m.Dimension):
    idVisit = m.Column(s.Integer, primary_key = True)

    serverDateTime = m.Column(s.DateTime)
    clientDateTime = m.Column(s.DateTime)

    actions = m.Column(s.Integer)
    browserCode = m.Column(s.String)
    browserFamily = m.Column(s.String)
    browserFamilyDescription = m.Column(s.String)
    browserName = m.Column(s.String)
    browserVersion = m.Column(s.String)

    city = m.Column(s.String)
    continent = m.Column(s.String)
    continentCode = m.Column(s.String)
    country = m.Column(s.String)
    countryCode = m.Column(s.String)

    daysSinceFirstVisit = m.Column(s.Integer)
    daysSinceLastVisit = m.Column(s.Integer)

    deviceType = m.Column(s.String)
    events = m.Column(s.Integer)

    idSite = m.Column(s.Integer)
    firstActionDate = m.Column(s.DateTime)
    lastActionDate = m.Column(s.DateTime)

    location = m.Column(s.String)
    latitude = m.Column(s.Float)
    longitude = m.Column(s.Float)

    operatingSystem = m.Column(s.String)
    operatingSystemCode = m.Column(s.String)
    operatingSystemShortName = m.Column(s.String)

#   plugins = 'pdf, flash, java, quicktime',

    provider = m.Column(s.String)
    providerName = m.Column(s.String)
    providerUrl = m.Column(s.String)
    referrerKeyword = m.Column(s.String)
    referrerKeywordPosition = m.Column(s.Integer, nullable = True),
    referrerName = m.Column(s.String)
    referrerSearchEngineUrl = m.Column(s.String, nullable = True),
    referrerType = m.Column(s.String)
    referrerTypeName = m.Column(s.String)
    referrerUrl = m.Column(s.String)
    region = m.Column(s.String)
    regionCode = m.Column(s.String)

    screen_width = m.Column(s.Integer)
    screen_height = m.Column(s.Integer)
    screenType = m.Column(s.String)
    searches = m.Column(s.Integer)
    visitCount = m.Column(s.Integer)
    visitDuration = m.Column(s.Integer)
    visitIp = m.Column(s.String)
    visitorId = m.Column(s.String)
    visitorType = m.Column(s.String)

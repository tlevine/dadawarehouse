import os
import datetime

from warehouse.logger import logger
from warehouse.db import Calendar, Event

CALENDARS = [os.path.join(os.path.expanduser('~/.pal'), rest) for rest in [\
    'secrets-nsa/secret-calendar.txt',
    'p/activities.txt',
    'p/to-do.txt',
    'p/sleeping.txt',
    'p/travel.txt',
    'p/postponed.txt',
]]
    
def update(session):
    for filename in CALENDARS:
        with open(filename) as fp:
            calendar, events = parse(fp)
        session.execute('DELETE FROM dim_calendar;')
        session.add(calendar)
        session.execute('DELETE FROM ft_calendar_event;')
        session.add_all(events)
        session.commit()
        logger.info('Inserted events from calendar %s' % filename)

def parse(fp, filename = None):
    'Read a pal calendar file.'
    if filename == None:
        try:
            filename = fp.name
        except NameError:
            raise ValueError('You must specify a filename.')
    calendar = None
    events = []

    for line in fp:
        line = line.rstrip()
        if line.startswith('#'):
            pass
        elif calendar == None:
            calendar_code, _, calendar_description = line.partition(' ')
            calendar = Calendar(code = calendar_code,
                                description = calendar_description,
                                filename = filename)
        else:
            events.extend((Event(calendar_code = calendar_code,
                                 event_date = date,
                                 event_description = description) \
                           for date, description in entry(line)))
    return calendar, events

def entry(line):
    'Read a pal calendar entry'
    datespec, _, description = line.partition(' ')
    for date in dates(datespec):
        yield date, description

def read_date(datestring):
    try:
        date = datetime.datetime.strptime(datestring, '%Y%m%d')
    except ValueError:
        return None
    else:
        return date.date()

def dates(datespec:str):
    single_date = read_date(datespec)
    if single_date != None:
        yield single_date
    elif datespec.count(':') == 2:
        subset, start, end = datespec.split(':')
        if subset == 'DAILY':
            today = read_date(start)
            end = read_date(end)
            while today <= end:
                yield today
                today += datetime.timedelta(days = 1)
    else:
        logger.warn('Unsupported date specification: "%s"' % datespec)

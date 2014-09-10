import os
import datetime

from ..logger import logger
import warehouse.model as m
from .model import File, CalendarEvent, Description

CALENDARS = [os.path.join(os.path.expanduser('~/.pal'), rest) for rest in [\
    'secrets-nsa/secret-calendar.txt',
    'p/activities.txt',
    'p/to-do.txt',
    'p/sleeping.txt',
    'p/travel.txt',
    'p/postponed.txt',
]]
    
def update(session, calendars = CALENDARS):
    session.query(Description).delete()
    session.query(CalendarEvent).delete()
    session.query(File).delete()
    session.commit()

    for filename in calendars:
        with open(filename) as fp:
            for thing in parse(fp):
                thing.merge(session)
        session.commit()
        logger.info('Inserted events from calendar %s' % filename)

def parse(fp, filename = None):
    'Read a pal calendar file.'

    # Parse the filename.
    if filename == None:
        try:
            filename = fp.name
        except NameError:
            raise ValueError('You must specify a filename.')

    calendar_file = None
    events = []
    for line in fp:
        line = line.rstrip()
        if line.startswith('#'):
            pass
        elif calendar_file == None:
            calendar_code, _, calendar_description = line.partition(' ')
            yield File(pk = calendar_code,
                filename = filename, description = calendar_description)
        else:
            date, description = entry(line)
            yield CalendarEvent(file = calendar_file, date_id = date,
                                description = description).merge(session)

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

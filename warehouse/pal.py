import os

from warehouse.db import Calendar, Event

CALENDARS = [os.path.join(os.path.expanduser('~/.pal'), rest) for rest in [\
    'secrets-nsa/secret-calendar.txt',
    'p/activities.txt',
    'p/to-do.txt',
    'p/birthdays.txt',
    'p/sleeping.txt',
    'p/travel.txt',
    'p/postponed.txt',
]]
    
def update(session):
    for filename in CALENDARS:
        with open(filename) as fp:
            calendar, events = parse(fp)
        session.add(calendar)
        calendar.add_all(events)

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
            events.extend(entry(line))
    return calendar, events

def entry(line):
    'Read a pal calendar entry'
    datespec, _, description = line.partition(' ')
    for date in dates(datespec):
        yield date, description

def dates(datespec:str):


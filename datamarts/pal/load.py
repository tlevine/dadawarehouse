import os
import datetime

from ..logger import logger
import warehouse.model as m
from .model import CalendarFile, CalendarEvent
from .parsers import entry, read_date, dates

CALENDARS = [os.path.join(os.path.expanduser('~/.pal'), rest) for rest in [\
    'secrets-nsa/secret-calendar.pal',
    'p/activities.pal',
    'p/to-do.pal',
    'p/sleeping.pal',
    'p/travel.pal',
    'p/postponed.pal',
]]
    
def update(session, calendars = CALENDARS):
    session.query(CalendarEvent).delete()
    session.query(CalendarFile).delete()

    for filename in calendars:

        if filename == None:
            try:
                filename = fp.name
            except NameError:
                raise ValueError('You must specify a filename.')

        todo = []
        with open(filename) as fp:
            for line in fp:
                line = line.rstrip()
                if line.startswith('#'):
                    pass
                elif len(todo) == 0:
                    calendar_code, _, calendar_description = line.partition(' ')
                    file_record = CalendarFile(
                        pk = calendar_code,
                        filename = filename,
                        description = calendar_description)
                    todo.append(file_record)
                else:
                    for date, description in entry(line):
                        todo.append(CalendarEvent(
                            file = file_record,
                            date = date,
                            description = calendar_description))

        session.add_all(todo)
        session.commit()
        logger.info('Inserted events from calendar %s' % filename)

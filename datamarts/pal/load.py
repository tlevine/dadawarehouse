import os
import datetime

from ..logger import logger
import doeund as m
from .model import PalFile, PalEvent
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
    session.query(PalEvent).delete()
    session.query(PalFile).delete()

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
                    file_record = PalFile(
                        pk = calendar_code,
                        filename = filename,
                        description = calendar_description)
                    todo.append(file_record)
                else:
                    for date, description in entry(line):
                        todo.append(PalEvent(
                            file = file_record,
                            date = date,
                            description = description))

        session.add_all(todo)
        session.commit()
        logger.info('Inserted events from calendar %s' % filename)

import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Event(Base):
    __tablename__ = 'ft_calendar_event'

    event_id = s.Column(s.Integer, primary_key = True)
    calendar_code = s.Column(s.String,
                             s.ForeignKey('dim_calendar.code'),
                             nullable=False)
    event_date = s.Column(s.DateTime, nullable = False)
    event_description = s.Column(s.String, nullable = False)

class Calendar(Base):
    __tablename__ = 'dim_calendar'

    code = s.Column(s.String(2), primary_key = True)
    description = s.Column(S.String, nullable = False)
    filename = s.Column(S.String, nullable = False)

def parse(fp, filename = fp.name):
    'Read a pal calendar file.'
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
    
    # session.drop( both of the tables)
    session.add(calendar)
    calendar.add_all(events)

def entry(line):
    'Read a pal calendar entry'
    datespec, _, description = line.partition(' ')
    for date in dates(datespec):
        yield date, description

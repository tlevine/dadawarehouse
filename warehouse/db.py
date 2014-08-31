import os

import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Shell(Base):
    __tablename__ = 'dim_shell'

    shell = s.Column(s.String(40), primary_key = True)
    shell_date = s.Column(s.DateTime(), nullable = False)

    def __repr__(self):
        return '<Shell(shell = "%s", shell_date = %s)>' % \
               (self.shell, self.shell_date)

class Command(Base):
    __tablename__ = 'command'
    command_id = s.Column(s.Integer, primary_key = True)
    shell = s.Column(s.String(40), s.ForeignKey('dim_shell.shell'), nullable=False)
    command_date = s.Column(s.DateTime, nullable = False)
    command = s.Column(s.String, nullable = False)
    def __repr__(self):
        return '<Command(shell = "%s", command_date = %s, command = """%s""")>' % \
               (self.shell, self.command_date, self.command)

drop_ft_command = 'DROP VIEW IF EXISTS ft_command;'
create_ft_command = '''
CREATE VIEW ft_command AS
SELECT
  command_id, shell, command_date,
  strftime('%Y', command_date) 'year',
  strftime('%m', command_date) 'month',
  strftime('%d', command_date) 'day',
  strftime('%H', command_date) 'hour',
  strftime('%M', command_date) 'minute',
  strftime('%S', command_date) 'second',
  command
FROM command;
'''

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
    description = s.Column(s.String, nullable = False)
    filename = s.Column(s.String, nullable = False)

'''
class FacebookUser(Base):

class FacebookMessage(Base):
    __tablename__ = 'ft_facebook_message'

    user_id = s.Column(s.Integer, s.ForeignKey('ft_facebook_user.id'),
                       nullable = False)
    current_nick = s.Column(s.String, nullable = False)

CREATE TABLE log_msg (session TEXT, uid TEXT, nick TEXT, type TEXT, sent INT, ts INT, sentts INT, body TEXT);
CREATE TABLE log_status (session TEXT, uid TEXT, nick TEXT, ts INT, status TEXT, desc TEXT);

'''

def session(cache_directory):
    database_file = os.path.join(cache_directory, 'dada.sqlite')
    engine = s.create_engine('sqlite:///' + database_file)
    Base.metadata.create_all(engine) 
    the_session = sessionmaker(bind=engine)()
    the_session.execute(drop_ft_command)
    the_session.execute(create_ft_command)
    return the_session

import os

import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Shell(Base):
    __tablename__ = 'shell'

    shell = s.Column(s.String(40), primary_key = True)
    shell_date = s.Column(s.DateTime(), nullable = False)

    def __repr__(self):
        return '<Shell(shell = "%s", shell_date = %s)>' % \
               (self.shell, self.shell_date)

class Command(Base):
    __tablename__ = 'ft_command'
    command_id = s.Column(s.Integer, primary_key = True)
    shell = s.Column(s.String(40), s.ForeignKey('shell.shell'), nullable=False)
    command_date = s.Column(s.DateTime, nullable = False)
    command = s.Column(s.String, nullable = False)
    def __repr__(self):
        return '<Command(shell = "%s", command_date = %s, command = """%s""")>' % \
               (self.shell, self.command_date, self.command)


drop_dim_shell = 'DROP VIEW IF EXISTS dim_shell;'
create_dim_shell = '''
CREATE VIEW dim_shell AS
SELECT
  shell.shell, shell.shell_date,
  max(ft_command.command_date) as 'final_command_date'
FROM ft_command
JOIN shell ON shell.shell = ft_command.shell
GROUP BY shell.shell;
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


def session(cache_directory):
    database_file = os.path.join(cache_directory, 'shell-history.sqlite')
    engine = s.create_engine('sqlite:///' + database_file)
    Base.metadata.create_all(engine) 
    the_session = sessionmaker(bind=engine)()
    the_session.execute(drop_dim_shell)
    the_session.execute(create_dim_shell)
    return the_session

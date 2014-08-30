import os

import sqlalchemy as s
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from historian_reader.shell import historian

Base = declarative_base()

class Shell(Base):
    __tablename__ = 'shells'

    shell = s.Column(s.String(40), primary_key = True)
    shell_date = s.Column(s.DateTime(), nullable = False)

    def __repr__(self):
        return '<Shell(shell = "%s", shell_date = %s)>' % \
               (self.shell, self.shell_date)

class Command(Base):
    __tablename__ = 'commands'
    shell = s.Column(s.String(40), s.ForeignKey('shells.shell'),
                       nullable=False),
    command_date = s.Column(s.DateTime, nullable = False),
    command = s.Column(s.String, nullable = False),
    def __repr__(self):
        return '<Command(shell = "%s", command_date = %s, command = """%s""")>' % \
               (self.shell, self.command_date, self.command)


def session(cache_directory):
    database_file = os.path.join(cache_directory, 'shell-history.sqlite')
    engine = create_engine('sqlite:///' + database_file)
    return sessionmaker(bind=engine)
   #metadata.create_all(engine)

def update(session):
    HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')
    previous_shells = session.query(Shell.shell)
    for shell in historian(directory = HISTORY, skip = previous_shells):
        session.add(Shell(shell = shell['shell'],
                          shell_date = shell['shell_date']))
        session.add_all((Command(shell = shell['shell'],
                                 command_date = command_date,
                                 command = command_string,
                ) for command_date, command_string in shell['commands']))
        session.commit()

def run(cache_directory):
    update(session(cache_directory))

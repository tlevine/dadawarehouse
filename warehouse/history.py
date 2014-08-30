import os

import sqlalchemy as s

from historian_reader.shell import historian

HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')


metadata = s.MetaData()

sessions = s.Table('sessions', metadata,
    s.Column('session', s.String(40), primary_key = True),
    s.Column('session_date', s.DateTime(), nullable = False),
)

commands = s.Table('commands', metadata,
    s.Column('session', s.String(40), s.ForeignKey('sessions.session'),
             nullable=False),
    s.Column('command_date', s.DateTime, nullable = False),
    s.Column('command', s.String, nullable = False),
)

def connect(cache_directory):
    database_file = os.path.join(cache_directory, 'shell-history.sqlite')
    engine = create_engine('sqlite:///' + database_file)
    metadata.create_all(engine)

def update(sessions_table):
    previous_sessions = sessions_table.distinct('session')
    for session in historian(directory = HISTORY, skip = previous_sessions):
        rows = ({
                    'session': session['session'],
                    'session_date': session['session_date'],
                    'command_date': command_date,
                    'command': command_string,
                } for command_date, command_string in session['commands'])
        sessions_table.insert_many(rows)

def run(cache_directory):
    update(connect(cache_directory))

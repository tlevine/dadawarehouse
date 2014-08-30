import os

import dataset

from historian_reader.shell import historian

HISTORY = os.path.join(os.path.expanduser('~'), 'history', 'shell')

def connect(cache_directory):
    database_file = os.path.join(cache_directory, 'shell-history.sqlite')
    db = dataset.connect('sqlite:///' + database_file)
    if 'sessions' not in db.tables:
        sessions = db.create_table('sessions', primary_id = 'session')
    else:
        sessions = db['sessions']
    return sessions

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

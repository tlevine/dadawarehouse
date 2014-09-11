from collections import defaultdict
from itertools import chain
import shutil
import os
import re
import datetime
import subprocess

import sqlalchemy

from ..logger import logger
from .model import LogSqliteDb, \
                   FacebookChatStatusChange, FacebookMessage, \
                   FacebookDuration
from ..model import Date, DateTime

WAREHOUSE = os.path.expanduser('~/.dadawarehouse')
LOCAL_CHAT = os.path.join(WAREHOUSE, 'facebookchat')
REMOTE_CHAT = 'safe:rsync/ekg2-logs/xmpp:perluette@chat.facebook.com/*.db'
RSYNC = ['rsync', '--archive', '--sparse'] #, '--verbose']

def download():
    if not os.path.isdir(LOCAL_CHAT):
        os.mkdir(LOCAL_CHAT)
    rsync = subprocess.Popen(RSYNC + [REMOTE_CHAT, LOCAL_CHAT])
    rsync.wait()

UID = re.compile(r'xmpp:-([0-9]+)@chat.facebook.com')
def parse_uid(uid):
    return str(int(re.match(UID, uid).group(1)))

def status_changes(engine, filedate_id, session):
    sql = 'SELECT rowid, uid, nick, ts, status FROM log_status'
    for rowid, uid, nick, ts, status in engine.execute(sql).fetchall():
        yield FacebookChatStatusChange(
            filedate_id = filedate_id,
            rowid = rowid,
            user_id = parse_uid(uid),
            datetime_id = datetime.datetime.fromtimestamp(ts),
            current_name = nick,
            status = status)

def messages(engine, filedate_id, session):
    sql = 'SELECT rowid, uid, nick, ts, body FROM log_msg'
    for rowid, uid, nick, ts, body in engine.execute(sql).fetchall():
        yield FacebookMessage(
            filedate_id = filedate_id,
            rowid = rowid,
            user_id = parse_uid(uid),
            datetime = datetime.datetime.fromtimestamp(ts),
            current_name = nick,
            body = body)

def online_durations(engine, filedate_id, session):
    for uid, nick in engine.execute('SELECT DISTINCT uid, nick FROM log_status;'):
        duration = 0
        avail = False
        prev_ts = None
        for ts, status in engine.execute('SELECT ts, status FROM log_status WHERE uid = ? ORDER BY ts', uid):
            if status == 'avail' and not avail:
                avail = True
                prev_ts = ts
            elif status == 'avail' and avail:
                pass
            elif status == 'avail' and not avail:
                avail = True
                prev_ts = ts
            elif status == 'notavail' and not avail:
                pass
            elif status == 'notavail' and avail:
                duration += ts - prev_ts
                avail = False
                prev_ts = None
            elif status == 'notavail' and not avail:
                pass
            else:
                raise AssertionError('This else condition shouldn\'t happen.')

        yield FacebookDuration(
            date = filedate_id,
            user = parse_uid(uid),
            duration = duration
        )

def update(session, today = datetime.date.today()):
 #  download()
    already_imported = session.query(LogSqliteDb.filedate_id).distinct()
    for filename in set(os.listdir(LOCAL_CHAT)).difference(already_imported):
        try:
            filedate_id = datetime.datetime.strptime(filename, '%Y-%m-%d.db').date()
            if filedate_id >= today:
                # Skip if it's from today because the file might not be complete.
                continue
            logger.info('Importing %s' % filename)

            # Copy to RAM so it's faster.
            shutil.copy(os.path.join(LOCAL_CHAT, filename), '/tmp/fb.db')
            engine = sqlalchemy.create_engine('sqlite:////tmp/fb.db')


            # Add stuff
            session.add_all(status_changes(engine, filedate_id, session))
            FacebookChatStatusChange.create_related(session)
            session.add_all(messages(engine, filedate_id, session))
            FacebookMessage.create_related(session)
            session.add_all(online_durations(engine, filedate_id, session))
            FacebookDuration.create_related(session)
            session.add(LogSqliteDb(filedate_id = filedate_id))

            # Commit at the end so that we can't have a partial import
            # for a given day.
            session.commit()
            logger.info('Finished %s' % filename)
        except KeyboardInterrupt:
            break

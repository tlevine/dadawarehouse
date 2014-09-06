from collections import defaultdict
import os
import re
import datetime
import subprocess

import sqlalchemy

from ..logger import logger
from .model import FacebookUser, FacebookUserNick, \
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

def get_user_nicks(engine):
    for uid, nick in engine.execute('SELECT DISTINCT * FROM (SELECT uid, nick FROM log_status UNION SELECT uid, nick FROM log_msg);'):
        user = FacebookUser(pk = parse_uid(uid), current_nick = nick)
        yield FacebookUserNick(user = user, nick = nick)

def convert_log(engine, filedate):
    for row in engine.execute('SELECT rowid, uid, nick, ts, status FROM log_status').fetchall():
        rowid, uid, nick, ts, status = row
        yield FacebookChatStatusChange(
            filedate = Date(pk = filedate),
            rowid = rowid,
            user = FacebookUser(pk = parse_uid(uid), current_nick = nick),
            datetime = DateTime(pk = datetime.datetime.fromtimestamp(ts)),
            status = status)

    for row in engine.execute('SELECT rowid, uid, nick, ts, body FROM log_msg').fetchall():
        rowid, uid, nick, ts, body = row
        yield FacebookMessage(
            filedate = Date(pk = filedate),
            rowid = rowid,
            user = FacebookUser(pk = parse_uid(uid), current_nick = nick),
            datetime = DateTime(pk = datetime.datetime.fromtimestamp(ts)),
            body = body)

def online_durations(engine, filedate):
    counts = defaultdict(lambda: {'avail': 0, 'notavail': 0})
    for uid, status, count in 'select uid, status, count(*) from log_status group by uid, status;':
        counts[uid][status] = count

    equal_count = '''
SELECT ends.uid, nick, ends.ends - beginnings.beginnings
FROM (
  SELECT nick, uid, sum(ts) 'ends'
  FROM log_status
  WHERE status = 'notavail'
  GROUP BY uid
) 'ends'
JOIN (
  SELECT uid, sum(ts) 'beginnings'
  FROM log_status
  WHERE status = 'avail'
  GROUP BY uid
) 'beginnings'
ON ends.uid = beginnings.uid;
'''
    for uid, nick, duration in engine.execute(sql).fetchall():
        if counts[uid]['avail'] == counts[uid]['notavail']:
            yield FacebookDuration(date = Date(pk = filedate),
                user = FacebookUser(pk = parse_uid(uid), current_nick = nick),
                duration = duration)
        else:
            first_sql = 'SELECT status FROM log_status WHERE uid = ? ORDER BY ts ASC LIMIT 1'
            last_sql = 'SELECT status FROM log_status WHERE uid = ? ORDER BY ts DESC LIMIT 1'
            first_status = engine.execute(first_sql).fetchone()[0]
            last_status = engine.execute(last_sql).fetchone()[0]
            if first_status == 'notavail':
                sql = 'SELECT sum(

def update(session):
    download()
    for filename in os.listdir(LOCAL_CHAT):
        try:
            filedate = datetime.datetime.strptime(filename, '%Y-%m-%d.db').date()
            is_new = session.query(FacebookChatStatusChange).\
                filter(FacebookChatStatusChange.filedate_id == filedate).\
                count() == 0
            if is_new:
                logger.info('Importing %s' % filename)
                engine = sqlalchemy.create_engine('sqlite:///' +
                    os.path.join(LOCAL_CHAT, filename))

                # This paragraph is for testing.
              # session.add(next(convert_log(engine, filedate)).link(session))
              # session.commit()
              # session.add(next(get_user_nicks(engine)).link(session))
              # session.commit()
              # assert False
                session.add_all(duration.link(session) for duration in online_durations(engine, filedate))
                session.add_all(user_nick.link(session) for user_nick in get_user_nicks(engine))
                session.add_all(log_event.link(session) for log_event in convert_log(engine, filedate))
                session.commit()
                logger.info('Finished %s' % filename)
            else:
                logger.info('Skipping %s' % filename)
        except KeyboardInterrupt:
            break

# Schema notes
#
# CREATE TABLE log_msg (session TEXT, uid TEXT, nick TEXT, type TEXT, sent INT, ts INT, sentts INT, body TEXT);
# "session" is always the same
# "type" is always "chat"
# "sent" is always 0
# "ts" versus "sentts"? maybe ts is the date it was written?
#
# CREATE TABLE log_status (session TEXT, uid TEXT, nick TEXT, ts INT, status TEXT, desc TEXT);
# "session" is always the same
# "desc" is always empty.

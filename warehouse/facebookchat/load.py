import os
import re
import datetime
import subprocess

import sqlalchemy

from .logger import logger
from .model import FacebookChatStatus, FacebookMessage

WAREHOUSE = os.path.expanduser('~/.dadawarehouse')
LOCAL_CHAT = os.path.join(WAREHOUSE, 'facebookchat')
REMOTE_CHAT = 'safe:rsync/ekg2-logs/xmpp:perluette@chat.facebook.com/*.db'
RSYNC = ['rsync', '--archive', '--sparse'] #, '--verbose']

def download():
    if not os.path.isdir(LOCAL_CHAT):
        os.mkdir(LOCAL_CHAT)
    scp = subprocess.Popen(RSYNC + [REMOTE_CHAT, LOCAL_CHAT])
    scp.wait()

UID = re.compile(r'xmpp:-([0-9]+)@chat.facebook.com')
def parse_uid(uid):
    return int(re.match(UID, uid).group(1))

def convert_log(engine, file_date):
    for row in engine.execute('SELECT rowid, uid, nick, ts, status FROM log_status').fetchall():
        rowid, uid, nick, ts, status = row
        yield FacebookChatStatus(
            status_id = rowid,
            file_date = file_date,
            user_id = parse_uid(uid),
            current_nick = nick,
            date = datetime.datetime.fromtimestamp(ts),
            status = status)
    for row in engine.execute('SELECT rowid, uid, nick, ts, body FROM log_msg').fetchall():
        rowid, uid, nick, ts, body = row
        yield FacebookMessage(
            file_date = file_date,
            message_id = rowid,
            user_id = parse_uid(uid),
            current_nick = nick,
            date = datetime.datetime.fromtimestamp(ts),
            body = body)

def update(session):
    download()
    for filename in os.listdir(LOCAL_CHAT):
        try:
            file_date = datetime.datetime.strptime(filename, '%Y-%m-%d.db').date()
            is_new = session.query(FacebookChatStatus).\
                filter(FacebookChatStatus.file_date == file_date).\
                count() == 0
            if is_new:
                logger.info('Importing %s' % filename)
                engine = sqlalchemy.create_engine('sqlite:///' +
                    os.path.join(LOCAL_CHAT, filename))
                session.add_all(convert_log(engine, file_date))
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

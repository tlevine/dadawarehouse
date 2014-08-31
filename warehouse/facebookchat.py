import os
import re
import datetime
import subprocess

import sqlalchemy
from .db import FacebookChatStatus, FacebookMessage

WAREHOUSE = os.path.expanduser('~/.dadawarehouse')
LOCAL_CHAT = os.path.join(WAREHOUSE, 'facebookchat')
REMOTE_CHAT = 'safe:rsync/ekg2-logs/xmpp:perluette@chat.facebook.com/*.db'
RSYNC = ['rsync', '--archive', '--sparse'] #, '--verbose']

RESULT = 'sqlite:////home/tlevine/.dadawarehouse/dada.sqlite'
TMP = '/tmp/facebookchat.sqlite' 

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
  # download()
    for filename in os.listdir(LOCAL_CHAT):
        file_date = datetime.datetime.strptime(filename, '%Y-%m-%d.db').date()
        is_new = session.query(FacebookChatStatus).\
            filter(FacebookChatStatus.file_date == file_date).\
            count() == 0
        if is_new:
            engine = sqlalchemy.create_engine('sqlite:///' +
                os.path.join(LOCAL_CHAT, filename))
            session.add_all(convert_log(engine, file_date))
            session.commit()

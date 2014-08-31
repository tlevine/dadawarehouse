import os
import shutil
import subprocess

import sqlalchemy

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

def union(sources:str, destination:str):
    sql = '''\
CREATE TABLE log_msg (session TEXT, uid TEXT, nick TEXT, type TEXT, sent INT, ts INT, sentts INT, body TEXT);
CREATE TABLE log_status (session TEXT, uid TEXT, nick TEXT, ts INT, status TEXT, desc TEXT);
CREATE INDEX ts ON log_msg(ts);
CREATE INDEX uid_ts ON log_msg(uid, ts);'''
    for source in sources:
        sql += '''\
ATTACH DATABASE '%s' AS today;
BEGIN TRANSACTION;
INSERT INTO log_msg SELECT * FROM today.log_msg;
INSERT INTO log_status SELECT * FROM today.log_status;
COMMIT TRANSACTION;
DETACH DATABASE today;
''' % source
    sqlite3 = subprocess.Popen(['sqlite3', destination], stdin = subprocess.PIPE)
    sqlite3.stdin.write(sql.encode('latin1'))
    sqlite3.wait()

def update(session):
  # download()
    daily_logs = (os.path.join(LOCAL_CHAT, fn) for fn in os.listdir(LOCAL_CHAT))
    if os.path.exists(TMP):
        raise ValueError(TMP + ' exists')
    else:
        union(daily_logs, TMP)

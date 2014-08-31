import os
import shutil
import subprocess

import sqlalchemy
import bubbles

WAREHOUSE = os.path.expanduser('~/.dadawarehouse')
LOCAL_CHAT = os.path.join(WAREHOUSE, 'facebookchat')
REMOTE_CHAT = 'safe:rsync/ekg2-logs/xmpp:perluette@chat.facebook.com/*.db'
RSYNC = ['rsync', '--archive', '--sparse'] #, '--verbose']

RESULT = 'sqlite:////home/tlevine/.dadawarehouse/dada.sqlite'
TMP = 'sqlite:////tmp/facebookchat.sqlite'

def download():
    if not os.path.isdir(LOCAL_CHAT):
        os.mkdir(LOCAL_CHAT)
    scp = subprocess.Popen(RSYNC + [REMOTE_CHAT, LOCAL_CHAT])
    scp.wait()

def tmpdb():
    if not os.path.exists(TMP.replace('sqlite:///', '')):
        engine = sqlalchemy.create_engine(TMP)
        SCHEMA = [
            'CREATE TABLE log_msg (session TEXT, uid TEXT, nick TEXT, type TEXT, sent INT, ts INT, sentts INT, body TEXT);',
            'CREATE TABLE log_status (session TEXT, uid TEXT, nick TEXT, ts INT, status TEXT, desc TEXT);',
            'CREATE INDEX ts ON log_msg(ts);',
            'CREATE INDEX uid_ts ON log_msg(uid, ts);',
        ]
        for command in SCHEMA:
            engine.execute(command)
    return bubbles.open_store("sql", TMP)

def update(session):
    day_log = 'sqlite:////home/tlevine/.dadawarehouse/facebookchat/2013-11-25.db'
    log = bubbles.open_store('sql', day_log)

    p = bubbles.Pipeline(stores = {'tmp': tmpdb(), 'log': log})
    p.source('log', 'log_msg')
    p.insert_into('tmp', 'log_msg')
    p.run()


#   download()

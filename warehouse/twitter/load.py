import os, subprocess, json
import datetime

NOTMUCH = ['notmuch', 'show', '--format=json', 'from:twitter.com']
TMP = '/tmp/twitter'

def emails():
    if os.path.isfile(TMP):
        fp = open(TMP)
    else:
        raise NotImplementedError
        notmuch = subprocess.Popen(RSYNC)
        notmuch.wait()

    result = json.load(fp)
    fp.close()
    return result[1:] # The first is empty?

def update(session):
    for email in emails():
        subject = email[0][0]['headers']['Subject']
        date = datetime.datetime.fromtimestamp(email[0][0]['timestamp'])
        print(subject)

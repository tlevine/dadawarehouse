import os, subprocess, json
import re
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
        parse_subject(subject)

class actions:
    followed = re.compile(r'(^[^(]+) \(@([^)]+)\) is now following you on Twitter!$')
    mentioned = re.compile(r'(^[^(]+) \(@([^)]+)\) mentioned you on Twitter!$')
    replied = re.compile(r'(^[^(]+) \(@([^)]+)\) replied to one of your Tweets!')
    favorited = re.compile(r'(^[^(]+) \(@([^)]+)\) favorited one of your Tweets!')
    multiple = re.compile('Thomas Levine, you have new followers on Twitter!')

def parse_subject(subject):
    for action in [actions.followed, actions.mentioned,
                   actions.replied, actions.favorited]:
        m = re.match(action, subject)
        if m:
            return m.group(1), m.group(2), action
    if re.match(actions.multiple, subject):
        return None, None, actions.multiple
    else:
        raise ValueError('Could not parse subject "%s"' % subject)

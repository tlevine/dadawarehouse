import os, subprocess, json
import io
import re
import datetime

NOTMUCH = ['notmuch', 'show', '--format=json', 'from:twitter.com']
TMP = '/tmp/twitter'

def emails():
    if not os.path.isfile(TMP):
        with open(TMP, 'wb') as fp:
            notmuch = subprocess.Popen(NOTMUCH, stdout = fp,
                                       stderr = subprocess.PIPE)
        notmuch.wait()
    with open(TMP) as fp:
        result = json.load(fp)
    return result[1:] # The first is empty?

def update(session):
    for email in emails():
        subject = email[0][0]['headers']['Subject']
        date = datetime.datetime.fromtimestamp(email[0][0]['timestamp'])
        parse_subject(subject)

class actions:
    followed = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? is now following you on Twitter!$')
    mentioned = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? ?mentioned you on Twitter!')
    replied = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? replied to one of your Tweets!')
    favorited = re.compile(r'(?:(^[^(]+) \()@([^)]+)\)? favorited one of your Tweets!')
    multiple = re.compile('^Thomas Levine, you have new followers on Twitter!')
    retweeted = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? retweeted one of your (?:Ret|T)weets!')
    do_you_know = re.compile(r'^Do you know .+ on Twitter?')
    direct_message_old = re.compile(r'^Direct message from .+')
    direct_message = re.compile(r'(^[^(]+) \(@([^)]+)\) has sent you a direct message on Twitter!')

def parse_subject(subject):
    for action in [actions.followed, actions.mentioned, actions.direct_message,
                   actions.replied, actions.favorited, actions.retweeted]:
        m = re.match(action, subject)
        if m:
            return m.group(1), m.group(2), action

    for action in [actions.multiple, actions.do_you_know,
                   actions.direct_message_old]:
        if re.match(action, subject):
            return None, None, action
    
    import sys
    sys.stderr.write('Could not parse subject "%s"\n' % subject)
    return 8

import os, subprocess, json
import io
import re
import datetime

from .model import TwitterUser, TwitterAction
from ..model import DateTime

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
        filename = email[0][0][0]['filename']
        date = datetime.datetime.fromtimestamp(email[0][0]['timestamp'])
        name, handle, action = parse_subject(subject)
        yield TwitterAction(
            user = TwitterUser(handle = handle, name = name).link(session),
            action = ACTION_NAMES[action], email_file = filename,
            datetime = DateTime(pk = date).link(session)).link(session)

class actions:
    followed = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? is now following you on Twitter!$')
    followed_nameonly = re.compile(r'^([^)(@]+) is now following you on Twitter!')
    mentioned = re.compile(r'(?:(^[^(]+) ?\()?@([^)]+)\)? mentioned you on Twitter!')
    mentioned_photo = re.compile(r'(?:(^[^(]+) ?\()?@([^)]+)\)? mentioned you in a photo!')
    replied = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? replied to .+!')
    favorited = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? favorited .+\!')
    multiple = re.compile('^Thomas Levine, you have new followers on Twitter!')
    follower_in_body = re.compile(r'Thomas Levine, you have a new follower on Twitter!')
    retweeted = re.compile(r'(?:(^[^(]+) \()?@([^)]+)\)? retweeted .+!')
    do_you_know = re.compile(r'^Do you know .+ on Twitter?')
    direct_message_old = re.compile(r'^Direct message from .+')
    direct_message = re.compile(r'(^[^(]+) \(@([^)]+)\) has sent you a direct message on Twitter!')
ACTION_NAMES = {
    actions.followed: 'follow',
    actions.followed_nameonly: 'follow',
    actions.mentioned: 'mention',
    actions.mentioned_photo: 'mention',
    actions.replied: 'reply',
    actions.favorited: 'favorite',
    actions.retweeted: 'retweet',
    actions.direct_message: 'direct-message',
    actions.direct_message_old: 'direct-message',
}

def parse_subject(subject):
    for action in [actions.followed, actions.mentioned, actions.direct_message,
                   actions.replied, actions.favorited, actions.retweeted,
                   actions.mentioned_photo]:
        m = re.match(action, subject)
        if m:
            a, b, c = m.group(1), m.group(2), action
            break
    else:
        for action in [actions.multiple, actions.do_you_know,
            actions.follower_in_body, actions.direct_message_old]:
            if re.match(action, subject):
                a, b, c = None, None, action
                break
        else: 
            m = re.match(actions.followed_nameonly, subject)
            if m:
                a, b, c = m.group(1), None, actions.followed_nameonly
            else:
                logger.debug('Could not parse subject "%s"\n' % subject)
                a, b, c = None, None, None
    if a != None:
        a = a.strip()
    return a, b, c

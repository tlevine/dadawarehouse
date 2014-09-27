import os
import re
import datetime

from notmuch import Database, Query

from ..logger import logger
from .model import TwitterAction

def update(session):
    db = Database()
    q = session.query(TwitterAction.message_id)
    new_messages = Query(db, 'from:twitter.com').search_messages()
    old_message_ids = set(row[0] for row in q.distinct())
    session.add_all(twitter_actions(session, new_messages, old_message_ids))

def twitter_actions(session, new_messages, old_message_ids):
    for m in new_messages:
        message_id = m.get_message_id()
        if message_id in old_message_ids:
            logger.info('Already imported %s' % message_id)
        else:
            logger.info('Adding %s' % message_id)
            subject = m.get_header('subject')
            filename = m.get_filename()
            date = datetime.datetime.fromtimestamp(m.get_date())
            name, handle, action = parse_subject(subject)
            yield TwitterAction(user_handle = handle,
                                user_name = name,
                                action = ACTION_NAMES[action],
                                message_id = message_id,
                                datetime = date)
        try:
            session.commit()
        except Exception as e:
            logger.error(e)
            raise

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
    actions.multiple: None,
    actions.follower_in_body: None,
    actions.do_you_know: None,
    None: None,
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

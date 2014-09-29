from io import StringIO
import sys
import re
import datetime
from itertools import chain
import subprocess
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from notmuch import Database, Query
import pyzmail

import doeund as m

from ..logger import logger
from .model import NotmuchMessage, NotmuchAttachment

def update(sessionmaker):
    if offlineimap_is_running():
        raise EnvironmentError('In case offlineimap runs "notmuch new", you should stop offlineimap while importing data from notmuch.')
    q = sessionmaker().query(NotmuchMessage.message_id)
    past_messages = set(row[0] for row in q.distinct())

    # This would make things faster if my emails were on different SSDs.
    _update = partial(update_from_query, past_messages, sessionmaker)
    with ThreadPoolExecutor(25) as e:
        future = e.submit(_update, 'date:..2005')
        future.add_done_callback(_raise)
        for year in range(2006, datetime.date.today().year):
            future = e.submit(_update, 'date:%d..%d' % (year, year))
            future.add_done_callback(_raise)

def _raise(future):
    exception = future.exception()
    if exception != None:
        raise exception

def update_from_query(past_messages, sessionmaker, querystr):
    db = Database()
    session = sessionmaker()
    for m in Query(db,querystr).search_messages():
        message_id = m.get_message_id()
        if message_id in past_messages:
            logger.debug('Already imported %s' % message_id)
            continue
        past_messages.add(message_id)

        session.add(message(m))
        session.flush() # for foreign key constraints
        session.add_all(attachments(m))

        session.commit()
        logger.info('Added message "id:%s"' % m.get_message_id())

def offlineimap_is_running():
    pgrep = subprocess.Popen(['pgrep', 'offlineimap'], stdout = subprocess.PIPE)
    pgrep.wait()
    stdout, stderr = pgrep.communicate()
    return len(stdout) > 0

def addresses(m):
    headers = ['to', 'cc', 'bcc']
    with open(m.get_filename(), 'rb') as fp:
        pyzm = pyzmail.PyzMessage.factory(fp)

    tos = pyzm.get_addresses('to')
    if len(tos) == 0:
        from_name = from_address = None
    else:
        from_name, from_address = tos[0]

    recipients = list(zip(*chain(*(pyzm.get_addresses(header) for header in headers))))
    if len(recipients) == 0:
        recipient_names = recipient_addresses = []
    else:
        recipient_names, recipient_addresses = recipients

    return from_name, from_address, recipient_names, recipient_addresses


def message(m): 
    filename = m.get_filename()
    subject = m.get_header('subject')

    from_name, from_address, recipient_names, recipient_addresses = addresses(m)

    return NotmuchMessage(
        message_id = m.get_message_id(),
        datetime = datetime.datetime.fromtimestamp(m.get_date()),
        thread_id = m.get_thread_id(),
        filename = filename,
        subject = subject,
        from_name = from_name,
        from_address = from_address,
        recipient_names = recipient_names,
        recipient_addresses = recipient_names,
    )

def attachments(message):
    with open(message.get_filename(), 'rb') as fp:
        pyzm = pyzmail.PyzMessage.factory(fp)
    for part_number, part in enumerate(pyzm.mailparts):
        yield NotmuchAttachment(
            message_id = message.get_message_id(),
            part_number = part_number,
            content_type = part.type,
            name = part.filename,
        )

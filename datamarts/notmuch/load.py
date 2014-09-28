from io import StringIO
import sys
import re
import datetime
from itertools import chain
import subprocess

from notmuch import Database, Query
import pyzmail

import doeund as m

from ..logger import logger
from .model import NotmuchMessage, NotmuchAttachment

def update(session):
    if offlineimap_is_running():
        raise EnvironmentError('In case offlineimap runs "notmuch new", you should stop offlineimap while importing data from notmuch.')
    db = Database()
    q = session.query(NotmuchMessage.message_id)
    past_messages = set(row[0] for row in q.distinct())
    for m in Query(db,'').search_messages():
        message_id = m.get_message_id()
        if message_id in past_messages:
            logger.debug('Already imported %s' % message_id)
            continue

        session.add(message(session, m))
        session.flush() # for foreign key constraints
        session.add_all(attachments(session, m))

        past_messages.add(message_id)
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


def message(session, m): 
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

def attachments(session, message):
    with open(message.get_filename(), 'rb') as fp:
        pyzm = pyzmail.PyzMessage.factory(fp)
    for part_number, part in enumerate(pyzm.mailparts):
        yield NotmuchAttachment(
            message_id = message.get_message_id(),
            part_number = part_number,
            content_type = part.type,
            name = part.filename,
        )

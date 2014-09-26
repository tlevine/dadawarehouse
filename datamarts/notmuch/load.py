import re
import datetime
from itertools import chain

from notmuch import Database, Query
import pyzmail

import doeund as m

from ..logger import logger
from .model import EmailMessage, EmailAttachment, EmailCorrespondance

def update(session):
    db = Database()
    q = session.query(EmailMessage.message_id)
    past_messages = set(row[0] for row in q.distinct())
    for m in Query(db,'').search_messages():
        message_id = m.get_message_id()
        if message_id in past_messages:
        #   logger.info('Already imported %s' % message_id)
            continue

        session.add(message(session, m))
        session.flush() # for foreign key constraints
        session.add_all(attachments(session, m))
        session.add_all(correspondances(m))

        past_messages.add(message_id)
        session.commit()

      # logger.info('Added message "id:%s"' % m.get_message_id())

def correspondances(m):
    message_id = m.get_message_id()
    headers = ['to', 'cc', 'bcc']
    with open(m.get_filename(), 'rb') as fp:
        pyzm = pyzmail.PyzMessage.factory(fp)
        for from_name, from_address in pyzm.get_addresses('from'):
            to_pairs = chain(*(pyzm.get_addresses(header) for header in headers))
            for to_name, to_address in to_pairs:
                yield EmailCorrespondance(message_id = message_id,
                                          from_name = from_name,
                                          from_address = from_address,
                                          to_name = to_name,
                                          to_address = to_address)

def message(session, m): 
    filename = m.get_filename()
    subject = m.get_header('subject')

    name, address = parse_email_address(m.get_header('from'))

    return EmailMessage(
        message_id = m.get_message_id(),
        datetime = datetime.datetime.fromtimestamp(m.get_date()),
        thread_id = m.get_thread_id(),
        filename = filename,
        subject = subject,
        from_name = name,
        from_address = address,
    )

def attachments(session, message):
    try:
        for part_number, message_part in enumerate(message.get_message_parts()):
            content_type, name = parse_attachment_name(message_part)
            yield EmailAttachment(
                message_id = message.get_message_id(),
                part_number = part_number,
                content_type = content_type,
                name = name
            )
    except UnicodeDecodeError:
        logger.warning('Encoding error at message %s' % message.get_message_id())

def parse_email_address(email_address):
    'Return (name, email address)'
    match = re.match(r'(?:(.+) <)?([^>]+)>?', email_address)
    name = match.group(1)
    address = match.group(2)
    return name, address

def parse_attachment_name(headers):
    if headers.get('Content-Disposition') == 'inline':
        return None, None

    if 'Content-Type' in headers:
        match = re.match(r'([^;]+); name="([^"]+)"', headers['Content-Type'])
        if match:
            return match.group(1), match.group(2)

    if 'Content-Disposition' in headers:
        match = re.match(r'attachment; filename="([^"]+)"', headers['Content-Disposition'])
        if match:
            return None, match.group(1)

    return None, None

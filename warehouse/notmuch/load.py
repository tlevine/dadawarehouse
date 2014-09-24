import re
import datetime

from notmuch import Database, Query

import warehouse.model as m

from ..logger import logger
from .model import EmailMessage, EmailAttachment, EmailCorrespondance

def update(session):
    db = Database()
    q = session.query(EmailMessage.filename)
    past_messages = set(row[0] for row in q.distinct())
    for m in Query(db,'').search_messages():
        fn = m.get_filename()
        if fn in past_messages:
            logger.info('Already imported %s' % fn)
            continue

        message(session, m)
        session.add_all(attachments(session, m))
        session.add_all(correspondance(m))

        past_messages.add(m.get_message_id())
        session.commit()

        logger.info('Added message "id:%s"' % m.get_message_id())

def correspondances(m):
    return []

def message(session, m): 
    filename = m.get_filename()
    subject = m.get_header('subject')

    name, address = parse_email_address(m.get_header('from'))

    return Message(
        notmuch_message_id = m.get_message_id(),
        datetime_id = datetime.datetime.fromtimestamp(m.get_date()),
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
            yield NotmuchAttachment(
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

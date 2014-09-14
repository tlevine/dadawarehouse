import re
import datetime

from notmuch import Database, Query

import warehouse.model as m

from ..logger import logger
from .model import NotmuchMessage, NotmuchAttachment, NotmuchCorrespondance,\
                   AddressName, Name, Address, Message, ContentType

def update(session):
    db = Database()
    past_messages = set(row[0] for row in session.query(Message.filename).distinct())
    for m in Query(db,'').search_messages():
        fn = m.get_filename()
        if fn in past_messages:
            logger.info('Already imported %s' % fn)
            continue

        message(session, m)
        Message.create_related(session)

#       session.add_all(attachments(session, m))
#       NotmuchAttachment.create_related(session)

#       session.add_all(correspondance(m))
#       NotmuchCorrespondance.create_related(session)

        past_messages.add(m.get_message_id())
        session.commit()
        logger.info('Added message "id:%s"' % m.get_message_id())

def correspondance(m):
    return []

def message(session, m): 
    filename = m.get_filename()
    subject = m.get_header('subject')

    name, address = parse_email_address(m.get_header('from'))
    address_id = Address.from_label(session, address)
    name_id = Name.from_label(session, name)

    AddressName.from_label(session, address_id, name_id)

    dim_message = Message(
        notmuch_message_id = m.get_message_id(),
        datetime_id = datetime.datetime.fromtimestamp(m.get_date()),
        thread_id = m.get_thread_id(),
        filename = filename,
        subject = subject,
        from_address_id = address_id,
    )
    session.add(NotmuchMessage(message = dim_message))

def attachments(session, message):
    try:
        for part_number, message_part in enumerate(message.get_message_parts()):
            _content_type, name = parse_attachment_name(message_part)
            if _content_type == None:
                content_type_id = None
            else:
                content_type_id = ContentType.from_label(session, _content_type)
            yield NotmuchAttachment(
                message_id = message.get_message_id(),
                part_number = part_number,
                content_type_id = content_type_id,
                name = name
            )
    except UnicodeDecodeError:
        logger.warning('Encoding error at message %s' % message.get_message_id())

def parse_email_address(email_address):
    'Return (name, email address)'
    match = re.match(r'(?:(.+) <)?([^>]+)>?', email_address)
    name = match.group(2)
    address = match.group(1)
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

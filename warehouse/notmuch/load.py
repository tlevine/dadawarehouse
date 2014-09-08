import re
import datetime

from notmuch import Database, Query

import warehouse.model as m

from ..logger import logger
from .model import NotmuchMessage, NotmuchAttachment, NotmuchCorrespondance,\
                   Address, Thread, Message, ContentType

def update(session):
    db = Database()
    for message in Query(db,'').search_messages():
        _dt = datetime.datetime.fromtimestamp(message.get_date())
        dt = m.DateTime(pk = _dt)
        from_address = parse_email_address(message.get_header('from'))
        thread = Thread(pk = message.get_thread_id())
        filename = message.get_filename()
        subject = message.get_header('subject')

        dim_message = Message(
            pk = message.get_message_id(),
            datetime = dt,
            thread = thread,
            filename = filename,
            subject = subject,
            from_address = from_address,
        )
        session.add(NotmuchMessage(message = dim_message).link(session))
        session.commit()
        try:
            for part_number, message_part in enumerate(message.get_message_parts()):
                _content_type, name = parse_attachment_name(message_part)
                if _content_type == None:
                    content_type = None
                else:
                    content_type = ContentType(content_type = _content_type)
                session.add(NotmuchAttachment(
                    message = dim_message,
                    part_number = part_number,
                    content_type = content_type,
                    name = name
                ).link(session))
        except UnicodeDecodeError:
            logger.warning('Encoding error at message %s' % message.get_message_id())
            session.rollback()
        finally:
            session.commit()

def parse_email_address(email_address):
    match = re.match(r'(?:(.+) <)?([^>]+)>?', email_address)
    return Address(pk = match.group(2), name = match.group(1))

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

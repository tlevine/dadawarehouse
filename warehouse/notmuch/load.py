import re
import datetime

from notmuch import Database, Query

import warehouse.model as m

from .model import NotmuchMessage, NotmuchAttachment, NotmuchCorrespondance,\
                   Address, Thread, Message, ContentType

def update(session):
    db = Database()
    for message in Query(db,'').search_messages():
        _dt = datetime.datetime.fromtimestamp(message.get_date())
        dt = m.DateTime(pk = _dt).link(session)
        from_address = parse_email_address(message.get_header('from')).link(session)
        thread = Thread(pk = message.get_thread_id()).link(session)
        filename = message.get_filename()
        subject = message.get_header('subject')

        message = Message(
            pk = message.get_message_id(),
            datetime = dt,
            thread = thread,
            filename = filename,
            subject = subject,
            from_address = from_address,
        ).link(session)
        session.add(NotmuchMessage(message = message).link(session))
        for part_number, message_part in enumerate(message.get_message_parts()):
            content_type, name = parse_attachment_name(message_part)
            session.add(NotmuchAttachment(
                message = message,
                part_number = part_number,
                content_type = ContentType(content_type = content_type)\
                                   .link(session),
                name = name,
            ))
        session.commit()

def parse_email_address(email_address):
    match = re.match(r'([^<]+)?(?: <)?([^>]+)>?', email_address)
    return Address(pk = match.group(2), name = match.group(1))

def parse_attachment_name(headers):
    if headers.get('Content-Disposition') == 'inline':
        return None, None
    elif 'Content-Type' in headers:
        match = re.match(r'([^;]+); name="([^"]+)"', headers['Content-Type'])
        return match.group(1), match.group(2)
    elif 'Content-Disposition' in headers:
        match = re.match(r'attachment; filename="([^"]+)"', headers['Content-Disposition'])
        return None, match.group(1)
    else:
        return None, None

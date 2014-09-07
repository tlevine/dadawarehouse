from notmuch import Database, Query

import warehouse.model as m

from .model import NotmuchMessage, NotmuchAttachment, NotmuchCorrespondance,\
                   Address, Thread, Message, ContentType

def update(session):
    db = Database()
    for m in Query(db,'').search_messages()
        datetime = m.DateTime(
            pk = datetime.datetime.fromtimestamp(m.get_date())).link(session)
        from_address = parse_email_address(m.get_header('from')).link(session)
        thread = Thread(pk = m.get_thread_id()).link(session)
        filename = message.get_filename()
        subject = message.get_header('subject')

        message = Message(
            pk = m.get_message_id(),
            datetime = datetime,
            thread = thread,
            filename = filename,
            subject = subject,
            from_address = from_address,
        ).link(session)
        yield NotmuchMessage(message = message).link(session)
        for part_number, message_part in enumerate(m.get_message_parts()):
            content_type, name = parse_attachment_name(message_part)
            yield NotmuchAttachment(
                message = message,
                part_number = part_number,
                content_type = ContentType(content_type = content_type)\
                                   .link(session),
                name = name,
            )

def parse_email_address(email_address):
    m = re.match(r'([^<]+)?(?: <)?([^>]+)>?', email_address)
    return Address(pk = m.group(2), name = m.group(1))

def parse_attachment_name(headers):
    if headers.get('Content-Disposition') == 'inline':
        return None, None
    elif 'Content-Type' in headers:
        m = re.match(r'([^;]+); name="([^"]+)"', headers['Content-Type'])
        return m.group(1), m.group(2)
    elif 'Content-Disposition' in headers:
        m = re.match(r'attachment; filename="([^"]+)"', headers['Content-Disposition'])
        return None, m.group(1)
    else:
        return None, None

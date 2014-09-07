from notmuch import Database, Query

import warehouse.model as m

from .model import NotmuchMessage, NotmuchMessagePart, NotmuchCorrespondance,\
                   Address, Thread, Message

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
            yield NotmuchMessagePart(
                message = message,
                part_number = part_number,
                name = parse_attachment_name(message_part)
            )

def parse_email_address(email_address):
    m = re.match(r'([^<]+)?(?: <)?([^>]+)>?', email_address)
    return Address(pk = m.group(2), name = m.group(1))

def parse_attachment_name

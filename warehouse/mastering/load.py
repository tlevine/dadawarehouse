from ..facebookchat.model import FacebookMessage, FacebookChatStatusChange
from ..notmuch.model import EmailCorrespondance
from ..muttalias.model import MuttAlias

from .model import Person, EmailAddress

def update(session):
    for alias in session.query(MuttAlias).filter(MuttAlias.name != None):
        person = session.merge(Person(pk = alias.pk))
        if alias.email_address not in person.email_addresses:
            session.add(EmailAddress(person_id = alias.pk,
                                     email_address = alias.email_address))

from pylev import levenshtein

from ..facebookchat.model import FacebookMessage, FacebookChatStatusChange
from ..notmuch.model import EmailCorrespondance
from ..muttalias.model import MuttAlias

from .model import Person, EmailAddress

def update(session):
    # _mutt(session)
    _fb(session)

def _mutt(session):
    # Start with mutt aliases.
    for alias in session.query(MuttAlias).filter(MuttAlias.name != None):
        person = session.merge(Person(pk = alias.pk))
        if alias.email_address not in person.email_addresses:
            session.merge(EmailAddress(person_id = alias.pk,
                                       email_address = alias.email_address))
def _fb(session):
    q = session.query(FacebookMessage.user_id, FacebookMessage.current_name).distinct()
    for user_id, name in q:
        person_id = name.lower().replace(' ', '.')
        person = session.query(Person).filter(pk = person_id).first()
        if person == None:
            person = Person(pk 

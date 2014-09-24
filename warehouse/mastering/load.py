from collections import Counter

from pylev import levenshtein
from sqlalchemy import func as f

from ..logger import logger
from ..facebookchat.model import FacebookMessage, FacebookChatStatusChange
from ..notmuch.model import EmailCorrespondance
from ..muttalias.model import MuttAlias

from .model import Person, EmailAddress

def update(session):
    # _mutt(session)
    _fb(FacebookChatStatusChange, session)
    # _fb(FacebookMessage, session)

def _mutt(session):
    # Start with mutt aliases.
    for alias in session.query(MuttAlias).filter(MuttAlias.name != None):
        person = session.merge(Person(pk = alias.pk))
        if alias.email_address not in person.email_addresses:
            session.merge(EmailAddress(person_id = alias.pk,
                                       email_address = alias.email_address))

def _fb(Class, session):
    '''
    This index should help. ::

        CREATE INDEX facebook_status_current_name
        ON ft_facebookchatstatuschange (current_name);

    '''
    q = session.query(Class.user_id, Class.current_name)\
               .distinct()
    completed = defaultdict(lambda: set())
    for user_id, name in q:
        logger.debug('Checking Facebook user %d' % user_id)
        if name in completed and user_id not in completed[name]:
            logger.info('Skipping "%s" because multiple people have the name' % name)
        else:
            person_id = name.lower().replace(' ', '.')
            person = session.query(Person).filter(Person.pk = person_id).first()
            if person == None:
                session.add(Person(pk = person_id, facebook = user_id))
                session.commit()
                logger.info('Added %s' % person_id)

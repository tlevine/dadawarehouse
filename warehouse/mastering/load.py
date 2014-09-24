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
    q = session.query(Class.user_id, Class.current_name)\
               .distinct()
    logger.info('Making note of people with the same names')
    result = list(q)
    counts = Counter(name for uid, name in result)
    logger.info('Merging Facebook users')
    for user_id, name in result:
        logger.debug('Checking Facebook user %d' % user_id)
        if counts['name'] > 1:
            logger.info('Skipping "%s" because multiple people have the name' % name)
        else:
            person_id = name.lower().replace(' ', '.')
            person = session.query(Person).filter(pk = person_id).first()
            if person == None:
                session.add(Person(pk = person_id, facebook = user_id))
                session.commit()
                logger.info('Added %s' % person_id)

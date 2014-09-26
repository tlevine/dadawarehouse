from collections import Counter

from pylev import levenshtein
from unidecode import unidecode
from sqlalchemy import and_, or_

from ..logger import logger
from ..facebookchat.model import FacebookMessage, FacebookChatStatusChange
from ..notmuch.model import EmailCorrespondance
from ..muttalias.model import MuttAlias

from .model import ProtoMaster

def update(session):
#   _mutt(session)
#   _fb(FacebookMessage, session)
    _fb(FacebookChatStatusChange, session)

def _mutt(session):
    # Start with mutt aliases.
    condition = or_(ProtoMaster.context == 'muttalias_name',
                    ProtoMaster.context == 'muttalias_emailaddress')
    session.query(ProtoMaster).filter(condition).delete()
    session.flush()
    def go():
        for alias in session.query(MuttAlias).filter(MuttAlias.name != None):
            yield ProtoMaster(context = 'muttalias_name',
                              global_id = alias.pk,
                              local_id = alias.name)
            yield ProtoMaster(context = 'muttalias_emailaddress',
                              global_id = alias.pk,
                              local_id = alias.email_address)
            logger.info('Added %s' % alias.pk)
    session.add_all(go())
    session.commit()

def _fb(Class, session):
    '''
    This index should help. ::

        CREATE INDEX facebook_status_current_name
        ON ft_facebookchatstatuschange (current_name);

    Or maybe something like this
    https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/PostgreSQLInheritance
    '''
    q = session.query(Class.user_id, Class.current_name)\
               .distinct()
    completed = set()
    for user_id, name in q:
        logger.debug('Checking Facebook user %d' % user_id)
        if name in completed:
            logger.info('Skipping "%s" because someone else had that name too' % name)
        else:
            person_id = unidecode(name.lower().replace(' ', '.'))
            person = session.query(Person).filter(Person.facebook == user_id).first()
            if person == None:
                session.merge(Person(pk = person_id, facebook = user_id))
                logger.info('Added %s' % person_id)
            else:
                condition = and_(Names.name == name, Names.person_id == person.pk)
                if session.query(Names).filter(condition).first() == None:
                    session.add(Names(name = name, person_id = person.pk))
                    session.flush()
                    logger.info('Added a name for %s' % person.pk)
            completed.add(name)
    session.commit()

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
    _mutt(session)
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
    q = session.query(Class.user_id, Class.current_name)\
               .distinct()
    condition = or_(ProtoMaster.context == 'facebook_name',
                    ProtoMaster.context == 'facebook_id')
    session.query(ProtoMaster).filter(context).delete()
    session.flush()
    def go():
        for user_id, name in q:
            global_id = unidecode(name.lower().replace(' ', '.'))
            yield ProtoMaster(context = 'facebook_name',
                              local_id = name,
                              global_id = global_id)
            yield ProtoMaster(context = 'facebook_id',
                              local_id = user_id,
                              global_id = global_id)
            logger.info('Added %s from Facebook' % person.pk)
    session.add_all(go())
    session.commit()

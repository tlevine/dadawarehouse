import os
import re

from .model import MuttAlias
from ..logger import logger

def update(session):
    session.query(MuttAlias).delete()
    session.add_all(mutt_aliases())
    session.commit()
    logger.info('Updated mutt aliases')

def mutt_aliases():
    fn = os.path.expanduser('~/git/secrets-home/.mutt/aliases/people')
    identifiers = set()
    with open(fn, 'r') as fp:
        for line in fp:
            _, _, alias = line.partition(' ')
            identifier, _, name_address = alias.partition(' ')

            if identifier in identifiers:
                logger.info('Skipping duplicate entry for %s' % identifier)
                continue

            m = re.match(r'([^<]+)<([^>]+)>', name_address)
            if m != None:
                name, address = m.group(1), m.group(2)
            elif name_address.count(' ') == 0:
                name = None
                address = name_address
            else:
                raise ValueError('This address is unusual; fix it:\n%s' % name_address)
            yield MuttAlias(pk = identifier,
                            name = name,
                            email_address = address)
            identifiers.add(identifier)

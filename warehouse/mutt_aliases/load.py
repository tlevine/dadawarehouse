import os
import .model as m

from ..model.person import Person, EmailAddress

def mutt_aliases():
    fn = os.path.expanduser('~/git/secrets-home/.mutt/aliases/people')
    with open(fn, 'r') as fp:
        for line in fp:
            _, _, alias = line.partition(' ')
            identifier, _, address = alias.partition(' ')
            yield Person(pk = identifier)
            yield EmailAddress(email_address = address, person_id = person.identifier)

'''
Mappings between service-specific identifiers ("local_id")
and global identifiers ("person_id") for different services

The global identifier is in the format that I use in
my mutt alias file, which is approximately one of these.

* ``[first name].[last name]``
* ``[first name].[middle name].[last name]``
* ``[first name].[last name].[context, like a city]``

I use the last of these if the others would be ambiguous
because different people have the same name.
'''
import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Dimension, Column
from datamarts import (
    FacebookMessage, FacebookChatStatusChange,
    FacebookDuration, FacebookNameChange,
    MuttAlias,
    NotmuchMessage, NotmuchRecipient, NotmuchAttachment,
)

class Person(Dimension):
    person_id = Column(s.String, primary_key = True)

GidColumn = lambda: Column(s.String, s.ForeignKey(Person.person_id), nullable = True)

class Facebook(Dimension):
    person_id = GidColumn()
    local_id = Column(s.BigInteger, primary_key = True)

FacebookMessage.add_join([(FacebookMessage.user_id, Facebook.local_id)])
FacebookChatStatusChange.add_join([(FacebookChatStatusChange.user_id,
                                  Facebook.local_id)])
FacebookDuration.add_join([(FacebookDuration.user_id, Facebook.local_id)])
FacebookNameChange.add_join([(FacebookNameChange.user_id, Facebook.local_id)])

class Twitter(Dimension):
    person_id = GidColumn()
    person = relationship(Person)
    local_id = Column(s.String, primary_key = True)

class EmailAddress(Dimension):
    person_id = GidColumn()
    person = relationship(Person)
    local_id = Column(s.String, primary_key = True)

NotmuchMessage.add_join([(NotmuchMessage.from_address, EmailAddress.local_id)])
# NotmuchMessage.add_join(EmailAddress, [('to_address', 'email_address')])

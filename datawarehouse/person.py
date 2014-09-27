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
from sqlalchemy.dialects.postgres import ARRAY, CIDR

from doeund import Fact, Dimension, Column
from datamarts import (
    BranchableLog,
    FacebookMessage, FacebookChatStatusChange,
    FacebookDuration, FacebookNameChange,
    MuttAlias,
    NotmuchMessage, NotmuchRecipient, NotmuchAttachment,
    PiwikVisit,
)

def Array(columntype):
    return Column(ARRAY(columntype, dimensions = 1))

class Person(Fact):
    id = Column(s.String, primary_key = True)
    facebooks = Array(s.BigInteger)
    twitters = Array(s.String)
    email_addresses = Array(s.String)
    names = Array(s.String)
    ip_addresses = Array(CIDR)
    piwiks = Array(s.String)

FacebookMessage.add_join([(FacebookMessage.user_id, Person.facebooks)])
FacebookChatStatusChange.add_join([(FacebookChatStatusChange.user_id,
                                    Person.facebooks)])
FacebookDuration.add_join([(FacebookDuration.user_id, Person.facebooks)])
FacebookNameChange.add_join([(FacebookNameChange.user_id, Person.facebooks)])

NotmuchMessage.add_join([(NotmuchMessage.from_address, Person.email_addresses)])
NotmuchMessage.add_join([(NotmuchMessage.recipient_address, Person.email_addresses)])

NotmuchMessage.add_join([(NotmuchMessage.from_name, Person.names)])
NotmuchMessage.add_join([(NotmuchMessage.recipient_name, Person.names)])

BranchableLog.add_join([(BranchableLog.ip_address, Person.ip_addresses)])

PiwikVisit.add_join([(PiwikVisit.visitorId, Person.piwiks)])
PiwikVisit.add_join([(PiwikVisit.visitIp, Person.ip_addresses)])

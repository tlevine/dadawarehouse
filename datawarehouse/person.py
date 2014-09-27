'''
Mappings between service-specific identifiers and
global person identifiers for different services

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
from sqlalchemy.dialects.postgres import CIDR

from doeund import Fact, Dimension, Column
from datamarts import (
    BranchableLog,
    FacebookMessage, FacebookChatStatusChange,
    FacebookDuration, FacebookNameChange,
    MuttAlias,
    NotmuchMessage, NotmuchAttachment,
    PiwikVisit,
    TwitterAction
)
from .util import Array

class Person(Fact):
    '''
    If you have an attribute of a person and want to know the other
    attributes of the person, filter based on the columns in this table.

    If you have the global identifier of a person and want to filter
    another cube based on this identifier (treating person as a dimension),
    you should not use the columns in this table. Instead, you should use
    the appropriate dimension column within that cube. The cube is a view
    that recursively applies joins to denormalize a fact table, and this
    dimesion is included in that denormalized view.
    '''
    id = Column(s.String, primary_key = True)
    email_addresses = Array(s.String)
    names = Array(s.String)
    ip_addresses = Array(CIDR)
    piwiks = Array(s.String)
    facebooks = Array(s.BigInteger)
    twitters = Array(s.String)

PersonId = lambda: Column(s.String, s.ForeignKey(Person.id))

class EmailAddress(Dimension):
    emailaddress = Column(s.String, primary_key = True)
    person_id = PersonId()

NotmuchMessage.add_join([(NotmuchMessage.from_address, EmailAddress.emailaddress)])
NotmuchMessage.add_join([(NotmuchMessage.recipient_addresses, EmailAddress.emailaddress)])

BranchableLog.add_join([(BranchableLog.ip_address, Person.ip_addresses)])

PiwikVisit.add_join([(PiwikVisit.visitorId, Person.piwiks)])
PiwikVisit.add_join([(PiwikVisit.visitIp, Person.ip_addresses)])

TwitterAction.add_join([(TwitterAction.user_handle, Person.twitters)])

class Facebook(Dimension):
    id = Column(s.BigInteger, primary_key = True)
    person_id = PersonId()

FacebookMessage.add_join([(FacebookMessage.user_id, Facebook.id)])
FacebookChatStatusChange.add_join([(FacebookChatStatusChange.user_id,
                                    Facebook.id)])
FacebookDuration.add_join([(FacebookDuration.user_id, Facebook.id)])
FacebookNameChange.add_join([(FacebookNameChange.user_id, Facebook.id)])

Person.add_join([(Person.id, MuttAlias.pk)])

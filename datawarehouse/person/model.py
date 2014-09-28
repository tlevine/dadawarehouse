'''
Mappings between service-specific identifiers and
global person identifiers for different services

The global identifier is in the format that I use in
my mutt alias file, which is approximately one of these.

* ``[first name].[last name]``
* ``[first name].[middle name].[last name]``
* ``[nickname]``
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
    PiwikVisit, PiwikVisitorLocation,
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

def PersonId(*args, **kwargs):
    return Column(s.String, s.ForeignKey(Person.id), *args, **kwargs)

class EmailAddress(Dimension):
    emailaddress = Column(s.String, primary_key = True)
    person_id = PersonId()

NotmuchMessage.add_join([(NotmuchMessage.from_address, EmailAddress.emailaddress)])
NotmuchMessage.add_join([(NotmuchMessage.recipient_addresses, EmailAddress.emailaddress)])

class PersonLocation(Fact):
    'Populate this from a CSV file.'
    ip_address = Column(CIDR, primary_key = True)
    person_id = PersonId(primary_key = True)

# Union this table to the results of the following query.
#
# Join PersonLocation to PiwikVisitorLocation
# on PersonLocation.ip_address == PiwikVisitorLocation.ip_address,
# and select only the columns that are
# the final join targets from the columns in PersonLocation.
#
# This requires that joins be specified for all PersonLocation columns.
# Each join must involve only one column per table.
PersonLocation.add_union(
    [(PersonLocation.ip_address, PiwikVisitorLocation.ip_address)])

class PiwikVisitor(Dimension):
    id = Column(s.String, primary_key = True)
    person_id = PersonId()

PiwikVisit.add_join([(PiwikVisit.visitorId, PiwikVisitor.id)])
PiwikVisitorLocation.add_join(
    [(PiwikVisitorLocation.visitor_id, PiwikVisitor.id)])

class Twitter(Dimension):
    id = Column(s.String, primary_key = True)
    person_id = PersonId()

TwitterAction.add_join([(TwitterAction.user_handle, Twitter.id)])

class Facebook(Dimension):
    id = Column(s.BigInteger, primary_key = True)
    person_id = PersonId()

FacebookMessage.add_join([(FacebookMessage.user_id, Facebook.id)])
FacebookChatStatusChange.add_join([(FacebookChatStatusChange.user_id,
                                    Facebook.id)])
FacebookDuration.add_join([(FacebookDuration.user_id, Facebook.id)])
FacebookNameChange.add_join([(FacebookNameChange.user_id, Facebook.id)])

# I need to union all of these
class PersonName(Fact):
    'Populate this from a CSV file.'
    name = Column(s.String, primary_key = True)
    person_id = PersonId(primary_key = True)

TwitterNameHandle.add_join([(TwitterNameHandle.user_handle, Twitter.id)])
MuttAlias.add_join([(MuttAlias.pk, Person.id)])
FacebookNameChange.add_join([(FacebookNameChange.user_id, Facebook.id)])

# In the cube view, union to a bunch of other views.
# The cube is the table for the left column, and the
# selects are all the columns.
PersonName.union([(TwitterNameHandle.name, Person.id),
                  (MuttAlias.name, Person.id),
                  (FacebookNameChange.new_name, Person.id)])

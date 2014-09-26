import sqlalchemy as s

from doeund import Fact, Dimension
import doeund as m

Guid = s.String(32)

class Account(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)
    commodity_guid = m.Column(Guid)

    account_type = m.Column(s.String, nullable = True)
    section = m.Column(s.String, nullable = True)

class Transaction(Dimension):
    guid = m.Column(Guid, primary_key = True)
    currency = m.Column(Guid)
    post_date = m.Column(s.DateTime)
    enter_date = m.Column(s.DateTime)
    description = m.Column(s.String)

class Split(Fact):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(Account.guid))
    transaction_guid = m.Column(Guid, s.ForeignKey(Transaction.guid))
    memo = m.Column(s.String)
    value = m.Column(s.Float)
    value_num = m.Column(s.BigInteger, label = 'Numerator')
    value_denom = m.Column(s.BigInteger, label = 'Denominator')

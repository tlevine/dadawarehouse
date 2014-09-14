import sqlalchemy as s

from doeund import Fact, Dimension

import warehouse.model as m

Guid = s.String(32)

class AccountType(Dimension):
    guid = m.Column(Guid, primary_key = True)
    account_type = m.Column(s.String)

class Section(Dimension):
    guid = m.Column(Guid, primary_key = True)
    section = m.Column(s.String)

class Account(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)
    commodity_guid = m.Column(Guid)

    account_type_id = m.FkColumn(AccountType.guid, nullable = True)
    account_type = s.orm.relationship(AccountType)
    section_id = m.FkColumn(Section.guid, nullable = True)
    section = s.orm.relationship(Section)

class Transaction(Dimension):
    guid = m.Column(Guid, primary_key = True)
    currency = m.Column(Guid)
    post_date_id = m.DateTimeColumn()
    post_date = s.orm.relationship(m.DateTime, foreign_keys = [post_date_id])
    enter_date_id = m.DateTimeColumn()
    enter_date = s.orm.relationship(m.DateTime, foreign_keys = [enter_date_id])
    description = m.Column(s.String)

class GnuCashSplit(Fact):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(Account.guid))
    transaction_guid = m.Column(Guid, s.ForeignKey(Transaction.guid))
    memo = m.Column(s.String)
    value = m.Column(s.Float)
    value_num = m.Column(s.BigInteger, label = 'Numerator')
    value_denom = m.Column(s.BigInteger, label = 'Denominator')

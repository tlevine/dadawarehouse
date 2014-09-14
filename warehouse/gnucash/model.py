import sqlalchemy as s

from doeund import Fact, Dimension

import warehouse.model as m

Guid = s.String(32)

class AccountType(Dimension):
    pk = m.PkColumn()
    account_type = m.LabelColumn()

class Section(Dimension):
    pk = m.PkColumn()
    section = m.LabelColumn()

class Account(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)
    commodity_guid = m.Column(Guid)

    account_type = m.FkColumn(AccountType.pk)
    section = m.FkColumn(Section.pk)

class Transaction(Dimension):
    guid = m.Column(Guid, primary_key = True)
    currency = m.Column(Guid)
    post_date = m.DateTimeColumn()
    enter_date = m.DateTimeColumn()
    description = m.Column(s.String)

class GnuCashSplit(Fact):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(Account.guid))
    transaction_guid = m.Column(Guid, s.ForeignKey(Transaction.guid))
    memo = m.Column(s.String)
    value = m.Column(s.Float)
    value_num = m.Column(s.BigInteger, label = 'Numerator')
    value_denom = m.Column(s.BigInteger, label = 'Denominator')

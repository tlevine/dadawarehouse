import sqlalchemy as s

from doeund import Fact, Dimension

import warehouse.model as m

Guid = s.String(32)

class GnuCashAccountType(Dimension):
    pk = m.PkColumn()
    account_type = m.LabelColumn()

class GnuCashSection(Dimension):
    pk = m.PkColumn()
    section = m.LabelColumn()

class GnuCashSubSection(Dimension):
    pk = m.PkColumn()
    subsection = m.LabelColumn()

class GnuCashAccount(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)
    commodity_guid = m.Column(Guid)

    account_type = m.FkColumn(GnuCashAccountType.pk)
    section = m.FkColumn(GnuCashSection.pk)
    subsection = m.FkColumn(GnuCashSubSection.pk, nullable = True)

class GnuCashTransaction(Dimension):
    guid = m.Column(Guid, primary_key = True)
    currency = m.Column(Guid)
    post_date = m.DateTimeColumn()
    enter_date = m.DateTimeColumn()
    description = m.Column(s.String)

class GnuCashSplit(Fact):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(GnuCashAccount.guid))
    transaction_guid = m.Column(Guid, s.ForeignKey(GnuCashTransaction.guid))
    memo = m.Column(s.String)
    value_num = m.Column(s.BigInteger)
    value_denom = m.Column(s.BigInteger)

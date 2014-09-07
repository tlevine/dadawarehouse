from doeund import Fact, Dimension

import warehouse.model as m

Guid = s.String(32)

class GnuCashAccount(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)

    commodity_guid = m.Column(Guid)

class GnuCashHierarchy(Dimension):
    guid = m.Column(Guid, primary_key = True)

    account = m.Column(Guid, s.ForeignKey(GnuCashAccount.guid))
    section = m.Column(Guid, s.ForeignKey(GnuCashAccount.guid))
    subsection = m.Column(Guid, s.ForeignKey(GnuCashAccount.guid), nullable = True)

class GnuCashTransaction(Dimension):

class GnuCashSplit(Fact):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(Account.guid))
    memo = m.Column(s.String)
    value_num = m.Column(s.BigInteger)
    value_denom = m.Column(s.BigInteger)

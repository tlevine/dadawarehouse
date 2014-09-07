from doeund import Fact, Dimension

import warehouse.model as m

Guid = s.String(32)

class GnucashAccount(Dimension):
    guid = m.Column(Guid, primary_key = True)

    name = m.Column(s.String)
    code = m.Column(s.String)
    description = m.Column(s.String)

    account_type = m.Column(s.String)
    commodity_guid = m.Column(Guid)

    parent_guid = m.Column(Guid, s.ForeignKey(GnucashAccount.guid))

class GnucashSplit(Dimension):
    guid = m.Column(Guid, primary_key = True)
    account_guid = m.Column(Guid, s.ForeignKey(Account.guid))
    memo = m.Column(s.String)
    value_num = m.Column(s.BigInteger)
    value_denom = m.Column(s.BigInteger)

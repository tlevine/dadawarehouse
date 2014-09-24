

class EmailAddressName(m.Fact):
    __table_args__ = (s.UniqueConstraint('address', 'name'),)
    pk = m.PkColumn()
    address = m.Column(s.String)
    name = m.Column(s.String)

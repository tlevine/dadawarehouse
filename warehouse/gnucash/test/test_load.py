import datetime
from ..load import _parse_date

def test_parse_date():
    o = _parse_date('20131231000000')
    e = datetime.datetime(2013, 12, 31, 0, 0, 0)
    n.assert_equal(o, e)

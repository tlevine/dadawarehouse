import datetime

import nose.tools as n

from ..load import _parse_date

TESTCASES = [
    ('20131231000000', (2013, 12, 31, 0, 0, 0)),
]

def check_parse_date(raw, result):
    n.assert_equal(_parse_date(raw), datetime.datetime(*result))

def test_parse_date():
    for raw, result in TESTCASES:
        yield check_parse_date, raw, result

import nose.tools as n

from ..parse import parse

def test_parse():
    line = 'tlevine  pts/7        Fri Aug  1 10:05:24 2014 - Fri Aug  1 10:15:07 2014  (00:09)     178.36.15.241 via mosh [30685]\n'
    expectation = {
        'user': 'tlevine',
        'tty': 'pts/7',
        'ip_address': '178.36.15.241',
        'login_datetime': datetime.datetime(2014, 8, 1, 10, 5, 24),
        'logout_datetime': datetime.datetime(2014, 8, 1, 10, 15, 7),
    }
    n.assert_dict_equal(parse(line), expectation)

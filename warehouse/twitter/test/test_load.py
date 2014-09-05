import nose.tools as n

from ..load import parse_subject, actions

def check_parse_subject(testcase):
    subject, *expected = testcase
    n.assert_tuple_equal(parse_subject(subject), tuple(expected))

def test_parse_subject():
    for testcase in testcases:
        yield check_parse_subject, testcase
testcases = [
    ('Rebecca Williams (@internetrebecca) is now following you on Twitter!',
        'Rebecca Williams', 'internetrebecca', actions.followed),
    ('Volkan Unsal (@picardo) mentioned you on Twitter!',
        'Volkan Unsal', 'picardo', actions.mentioned),
    ('Burton DeWilde (@bjdewilde) replied to one of your Tweets!',
        'Burton DeWilde', 'bjdewilde', actions.replied),
    ('Burton DeWilde (@bjdewilde) favorited one of your Tweets!',
        'Burton DeWilde', 'bjdewilde', actions.favorited),
    ('Thomas Levine, you have new followers on Twitter!',
        None, None, actions.multiple),
]

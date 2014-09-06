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
    ('Arielle is now following you on Twitter!',
        None, None, actions.followed_old),
    ('Volkan Unsal (@picardo) mentioned you on Twitter!',
        'Volkan Unsal', 'picardo', actions.mentioned),
    ('Burton DeWilde (@bjdewilde) replied to one of your Tweets!',
        'Burton DeWilde', 'bjdewilde', actions.replied),
    ('Burton DeWilde (@bjdewilde) favorited one of your Tweets!',
        'Burton DeWilde', 'bjdewilde', actions.favorited),
    ('@seecmb retweeted one of your Retweets!',
        None, 'seecmb', actions.retweeted),
    ('Thomas Levine, you have new followers on Twitter!',
        None, None, actions.multiple),
    ('Do you know jimmy fallon, Justin Timberlake  and KATY PERRY  on Twitter?',
        None, None, actions.do_you_know),
    ('Dave Riordan (@riordan) has sent you a direct message on Twitter!',
        'Dave Riordan', 'riordan', actions.direct_message),
    ("Direct message from Carly Boxer",
        None, None, actions.direct_message_old),
    ("David Jones (@drjtwit) retweeted one of your Tweets!",
        'David Jones', 'drjtwit', actions.retweeted),
    ("ScraperWiki(@ScraperWiki) mentioned you on Twitter!",
        'ScraperWiki', 'ScraperWiki', actions.mentioned),
]

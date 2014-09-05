import nose.tools as n

from ..load import parse_subject, actions

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

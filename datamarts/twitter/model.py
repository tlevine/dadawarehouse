import os

import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Fact, PkColumn, Column

class TwitterAction(Fact):
    pk = PkColumn(hide = True)
    user_handle = Column(s.String, default = '')
    user_name = Column(s.String, default = '')
    datetime = Column(s.DateTime)
    action = Column(s.Enum('mention','favorite','retweet','follow','photo',
                           'reply', 'other', 'direct-message',
                           name = 'twitter_action'), default = 'other')
    message_id = Column(s.String)

class TwitterNameHandle(Fact):
    name = Column(s.String, primary_key = True)
    user_handle = Column(s.String, primary_key = True)

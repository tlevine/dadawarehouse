import os

import sqlalchemy as s
from sqlalchemy.orm import relationship

from doeund import Fact, PkColumn, Column

class TwitterAction(Fact):
    pk = PkColumn(hide = True)
    user_handle = Column(s.String)
    user_name = Column(s.String)
    datetime = Column(s.DateTime)
    action = Column(s.Enum('mention','favorite','retweet','follow','photo',
                             name = 'twitter_action'))
    message_id = Column(s.String)

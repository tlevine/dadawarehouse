import os

import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as m

class TwitterAction(m.Fact):
    pk = m.PkColumn()
    user_handle = s.Column(s.String, s.ForeignKey(m.Twitter.local_id))
    user_name = s.Column(s.String, s.ForeignKey(m.Name.name)
    datetime = m.Column(s.DateTime)
    action = s.Column(s.Enum('mention','favorite','retweet','follow','photo',
                             name = 'twitter_action'))
    message_id = s.Column(s.String)

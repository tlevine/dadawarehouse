import os

import sqlalchemy as s
from sqlalchemy.orm import relationship

import warehouse.model as m

class TwitterAction(m.Fact):
    pk = m.PkColumn()
    user_handle = s.Column(s.String)
    user_name = s.Column(s.String)
    datetime = m.Column(s.DateTime)
    action = s.Column(s.Enum('mention','favorite','retweet','follow','photo'))
    message_id = s.Column(s.String)

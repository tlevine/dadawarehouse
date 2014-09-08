import os

import sqlalchemy as s
from sqlalchemy.orm import relationship

import doeund as d

import warehouse.model as m

class TwitterUser(d.Dimension):
    handle = s.Column(s.String, primary_key = True)
    name = s.Column(s.String)

class TwitterAction(d.Fact):
    pk = m.PkColumn()
    user_id = s.Column(s.String, s.ForeignKey(TwitterUser.handle))
    user = relationship(TwitterUser)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    action = s.Column(s.Enum('mention','favorite','retweet','follow','photo'))
    email_file = s.Column(s.String)

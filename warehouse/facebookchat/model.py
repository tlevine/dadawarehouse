import os

from sqlalchemy.orm import relationship
import sqlalchemy as s

from doeund import Fact, Dimension, merge_on_unique

import warehouse.model as m

class FacebookUser(Dimension):
    pk = m.Column(s.String, primary_key = True)
    current_nick = m.Column(s.String)
    def link(self, session):
        return merge_on_unique(FacebookUser, session,
            FacebookUser.pk, self.pk)

class FacebookUserNick(Fact):
    pk = m.PkColumn()
    user_id = m.Column(s.String, s.ForeignKey(FacebookUser.pk))
    user = relationship(FacebookUser)
    nick = m.Column(s.String)
    def link(self, session):
        self.user = self.user.link(session)
        return self

class FacebookMessage(Fact):
    # Two-column primary key
    filedate = m.DateColumn(primary_key = True)
    rowid = m.Column(s.Integer, primary_key = True)

    user_id = m.Column(s.String, s.ForeignKey(FacebookUser.pk))
    user = relationship(FacebookUser)
    datetime = m.DateTimeColumn()
    body = m.Column(s.String)

    def link(self, session):
        self.user = self.user.link(session)
        return self

class FacebookChatStatusChange(Fact):
    # Two-column primary key
    filedate = m.DateColumn(primary_key = True)
    rowid = m.Column(s.Integer, primary_key = True)

    user_id = m.Column(s.String, s.ForeignKey(FacebookUser.pk))
    user = relationship(FacebookUser)
    datetime = m.DateTimeColumn()
    status = m.Column(s.Enum('avail','notavail', name = 'faceboook_chat_status'))

    def link(self, session):
        self.user = self.user.link(session)
        return self

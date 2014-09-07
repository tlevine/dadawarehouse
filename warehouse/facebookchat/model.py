import os

from sqlalchemy.orm import relationship
import sqlalchemy as s

from doeund import Fact, Dimension, merge_on_unique

import warehouse.model as m

class User(Dimension):
    user_id = m.Column(s.BigInteger, primary_key = True)
    current_nick = m.Column(s.String)
    def link(self, session):
        return merge_on_unique(User, session, User.user_id, self.user_id)

class FacebookUserFullName(Fact):
    pk = m.PkColumn()
    user_id = m.Column(s.BigInteger, s.ForeignKey(User.user_id))
    user = relationship(User)
    nick = m.Column(s.String, label = 'Full Name')
    def link(self, session):
        self.user = self.user.link(session)
        return self

class FacebookMessage(Fact):
    # Two-column primary key
    filedate_id = m.DateColumn(primary_key = True, label = 'File Date')
    filedate = relationship(m.Date)
    rowid = m.Column(s.Integer, primary_key = True, label = 'Row Id')

    user_id = m.Column(s.BigInteger, s.ForeignKey(User.user_id))
    user = relationship(User)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    body = m.Column(s.String)

    def link(self, session):
        self.user = self.user.link(session)
        self.filedate = self.filedate.link(session)
        self.datetime = self.datetime.link(session)
        return self

class FacebookChatStatusChange(Fact):
    # Two-column primary key
    filedate_id = m.DateColumn(primary_key = True, label = 'Log File Date')
    filedate = relationship(m.Date)
    rowid = m.Column(s.Integer, primary_key = True)

    user_id = m.Column(s.BigInteger, s.ForeignKey(User.user_id))
    user = relationship(User)
    datetime_id = m.DateTimeColumn()
    datetime = relationship(m.DateTime)
    status = m.Column(s.Enum('avail','notavail', name = 'faceboook_chat_status'),
                      label = 'New Status')

    def link(self, session):
        self.user = self.user.link(session)
        self.filedate = self.filedate.link(session)
        self.datetime = self.datetime.link(session)
        return self

class FacebookDuration(Fact):
    '''
    How long a person was on Facebook each day
    '''
    user_id = m.Column(s.BigInteger, s.ForeignKey(User.user_id), primary_key = True)
    user = relationship(User)
    date_id = m.DateColumn(primary_key = True)
    date = relationship(m.Date)
    duration = m.Column(s.Integer) # in seconds
    def link(self, session):
        self.date = self.date.link(session)
        self.user = self.user.link(session)
        return self

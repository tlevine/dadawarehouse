import os

import warehouse.model as m
from sqlalchemy import String

class FacebookUser(m.Dimension):
    pk = m.PkColumn()

class FacebookNick(m.Dimension):
    pk = m.PkColumn()
    nick = m.LabelColumn()

class FacebookChatStatus(m.Dimension):
    pk = m.PkColumn()
    status = m.LabelColumn()

class FacebookUserNick(m.Fact):
    pk = m.PkColumn()
    user = m.FkColumn(FacebookUser.pk)
    nick = m.FkColumn(FacebookNick.pk)

class FacebookMessage(m.Fact):
    pk = m.PkColumn()
    filedate = m.DateColumn()
    user = m.FkColumn(FacebookUser.pk)
    date = m.DateColumn()
    body = m.Column(String)

class FacebookChatStatusChange(m.Fact):
    # Two-column primary key
    filedate = m.DateColumn(primary_key = True)
    user = m.FkColumn(FacebookUser.pk)
    date = m.DateColumn()
    newstatus = m.FkColumn(FacebookChatStatus.pk)

import os

from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, BigInteger, Date, DateTime, Enum, ForeignKey

from warehouse.model import Fact, Dimension, Column

class FacebookUser(Dimension):
    pk = Column(String, primary_key = True)
    current_nick = Column(String)

class FacebookUserNick(Fact):
    user_id = Column(String, ForeignKey(FacebookUser.pk), primary_key = True)
    nick = Column(String, primary_key = True)

class FacebookMessage(Fact):
    # Two-column primary key
    filedate = Column(Date, primary_key = True)
    rowid = Column(Integer, primary_key = True)

    user_id = Column(String, ForeignKey(FacebookUser.pk))
    datetime = Column(DateTime)

    body = Column(String)

class FacebookChatStatusChange(Fact):
    # Two-column primary key
    filedate = Column(Date, primary_key = True)
    rowid = Column(Integer, primary_key = True)

    user_id = Column(String, ForeignKey(FacebookUser.pk))
    datetime = Column(DateTime)

    status = Column(Enum('avail','notavail', name = 'faceboook_chat_status'))

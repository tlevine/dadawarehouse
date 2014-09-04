import os

from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Date, DateTime, Enum, ForeignKey

from warehouse.model import Fact, Dimension, Column

class LogSqlite(Fact):
    __abstract__ = True

    # Two-column primary key
    filedate = Column(Date, primary_key = True)
    rowid = Column(Integer, primary_key = True)

    user = Column(Integer)
    current_nick = Column(String)
    datetime = Column(DateTime)

class FacebookMessage(LogSqlite):
    body = Column(String)

class FacebookChatStatusChange(LogSqlite):
    status = Column(Enum('avail','notavail', name = 'faceboook_chat_status'))

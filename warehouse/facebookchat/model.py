import os

import sqlalchemy as s

from .model import Fact, Dimension, Column, IdColumn, Date
from sqlalchemy import ForeignKey, String


class FacebookMessage(Fact):
    file_date = Column(s.Date, primary_key = True)
    message_id = Column(s.Integer, primary_key = True)
    user_id = Column(s.Integer, nullable = False)
    current_nick = Column(s.String, nullable = False)
    date = Column(s.DateTime, nullable = False)
    body = Column(s.String, nullable = False)

class FacebookChatStatus(Fact):
    file_date = Column(s.Date, primary_key = True)
    status_id = Column(s.Integer, primary_key = True)
    user_id = Column(s.Integer, nullable = False)
    current_nick = Column(s.String, nullable = False)
    date = Column(s.DateTime, nullable = False)
    status = Column(s.Enum('avail', 'notavail'), nullable = False)

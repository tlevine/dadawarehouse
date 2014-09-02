import os

import sqlalchemy as s
from doeund import Fact, Dimension, Column

class Shell(Dimension):
    shell = Column(s.String(40), primary_key = True)
    shell_date = Column(s.DateTime(), nullable = False)

class Command(Fact):
    command_id = Column(s.Integer, primary_key = True)
    shell = Column(s.String(40), s.ForeignKey(Shell.shell), nullable=False)
    command_date = Column(s.DateTime, nullable = False)
    command = Column(s.String, nullable = False)

class CalendarFile(Dimension):
    code = Column(s.String(2), primary_key = True)
    description = Column(s.String, nullable = False)
    filename = Column(s.String, nullable = False)

class CalendarEvent(Fact):
    event_id = Column(s.Integer, primary_key = True)
    calendar_code = Column(s.String(2),
                             s.ForeignKey(CalendarFile.code),
                             nullable=False)
    event_date = Column(s.DateTime, nullable = False)
    event_description = Column(s.String, nullable = False)

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

class Email(Fact):
    pass

import os

import sqlalchemy as s
from doeund import Fact, Dimension, Column

class Shell(Dimension):
    shell = Column(s.String(40), primary_key = True)
    shell_date = Column(s.DateTime(), nullable = False)

class Command(Base):
    __tablename__ = 'command'
    command_id = Column(s.Integer, primary_key = True)
    shell = Column(s.String(40), s.ForeignKey('dim_shell.shell'), nullable=False)
    command_date = Column(s.DateTime, nullable = False)
    command = Column(s.String, nullable = False)
    def __repr__(self):
        return '<Command(shell = "%s", command_date = %s, command = """%s""")>' % \
               (self.shell, self.command_date, self.command)

class Event(Base):
    __tablename__ = 'ft_calendar_event'

    event_id = Column(s.Integer, primary_key = True)
    calendar_code = Column(s.String,
                             s.ForeignKey('dim_calendar.code'),
                             nullable=False)
    event_date = Column(s.DateTime, nullable = False)
    event_description = Column(s.String, nullable = False)

class Calendar(Base):
    __tablename__ = 'dim_calendar'

    code = Column(s.String(2), primary_key = True)
    description = Column(s.String, nullable = False)
    filename = Column(s.String, nullable = False)

class FacebookMessage(Base):
    __tablename__ = 'ft_facebook_chat_message'

    file_date = Column(s.Date, primary_key = True)
    message_id = Column(s.Integer, primary_key = True)
    user_id = Column(s.Integer, nullable = False)
    current_nick = Column(s.String, nullable = False)
    date = Column(s.DateTime, nullable = False)
    body = Column(s.String, nullable = False)

    # CREATE TABLE log_msg (session TEXT, uid TEXT, nick TEXT, type TEXT, sent INT, ts INT, sentts INT, body TEXT);
    # "session" is always the same
    # "type" is always "chat"
    # "sent" is always 0
    # "ts" versus "sentts"? maybe ts is the date it was written?

    def __repr__(self):
        return '<FacebookMessage(file_date = %s, status_id = %d)>' % \
            (self.file_date, self.status_id)

class FacebookChatStatus(Base):
    __tablename__ = 'ft_facebook_chat_status'

    file_date = Column(s.Date, primary_key = True)
    status_id = Column(s.Integer, primary_key = True)
    user_id = Column(s.Integer, nullable = False)
    current_nick = Column(s.String, nullable = False)
    date = Column(s.DateTime, nullable = False)
    status = Column(s.Enum('avail', 'notavail'), nullable = False)

    # CREATE TABLE log_status (session TEXT, uid TEXT, nick TEXT, ts INT, status TEXT, desc TEXT);
    # "session" is always the same
    # "desc" is always empty.

    def __repr__(self):
        return '<FacebookMessage(file_date = %s, status_id = %d)>' % \
            (self.file_date, self.status_id)

class Email(Base):
    __tablename__ = 'ft_email'

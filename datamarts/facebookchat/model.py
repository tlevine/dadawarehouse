import os

import sqlalchemy as s

from ..model import Fact
import warehouse.model as m

class FacebookMessage(Fact):
    # Two-column primary key
    filedate = m.Column(s.Date, primary_key = True, label = 'File Date')
    rowid = m.Column(s.Integer, primary_key = True, label = 'Row Id')

    user_id = m.Column(s.BigInteger)
    datetime = m.Column(s.DateTime)
    current_name = m.Column(s.String, label = 'Full Name')
    body = m.Column(s.String)

  # Why doesn't this work???
  # @s.ext.declarative.declared_attr
  # def __table_args__(cls):
  #     return (s.schema.Index('%s_datetime' % cls.__tablename__, 'datetime'),)

class FacebookChatStatusChange(Fact):
    # Two-column primary key
    filedate = m.Column(s.Date, primary_key = True, label = 'File Date')
    rowid = m.Column(s.Integer, primary_key = True)

    user_id = m.Column(s.BigInteger)
    datetime = m.Column(s.DateTime)
    current_name = m.Column(s.String, label = 'Current Full Name')
    status = m.Column(s.Enum('avail','notavail', name = 'faceboook_chat_status'),
                      label = 'New Status')

class FacebookDuration(Fact):
    '''
    How long a person was on Facebook each day
    '''
    user_id = m.Column(s.BigInteger, primary_key = True)
    date = m.Column(s.Date, primary_key = True)
    duration = m.Column(s.Integer) # in seconds

class FacebookNameChange(Fact):
    pk = m.PkColumn()
    user_id = m.Column(s.BigInteger)
    datetime = m.Column(s.DateTime)
    new_name = m.Column(s.String)

import sqlalchemy as s
from doeund import Fact, Dimension, Column as _Column

def Column(*args, **kwargs):
    '''
    Column with good defaults
    '''
    _kwargs = dict(kwargs)
    if 'nullable' not in _kwargs:
        _kwargs['nullable'] = False
    return _Column(*args, **kwargs) 

def IdColumn(*args, **kwargs):
    '''
    Identifier field
    '''
    return Column(s.Integer, *args, **kwargs)

class Date(Dimension):
    '''
    Dates with hierarchies
    '''
    pk = Column(s.Date, primary_key = True)
    year = Column(s.Integer)
    month = Column(s.Integer)
    day = Column(s.Integer)

class Time(Dimension):
    pk = IdColumn(primary_key = True) # seconds from midnight
    hour = Column(s.Integer)
    minute = Column(s.Integer)
    second = Column(s.Integer)







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

#class Email(Fact):

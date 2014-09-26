import datetime
from functools import partial
import string

import pyparsing as p

from .model import BranchableLog

def _entry(parser, line):
    pyparse = parser.parseString(line)
    datestamp = pyparse['datetime'][0]
    dateformat = '%d/%b/%Y:%H:%M:%S'
    return BranchableLog(
        route = pyparse['requestURI'],
        status_code = pyparse['status_code'],
        ip_address = pyparse['ip_address'],
        datetime = datetime.datetime.strptime(datestamp, dateformat),
        user_agent = pyparse['user_agent'],
    )

def getCmdFields( s, l, t ):
    t["method"],t["requestURI"],t["protocolVersion"] = t[0].strip('"').split()

def get_pyparser():
    'http://pyparsing.wikispaces.com/file/view/httpServerLogParser.py/30166005/httpServerLogParser.py'
    integer = p.Word(p.nums)
    ipAddress = p.delimitedList(integer, ".", combine=True)
    timeZoneOffset = p.Word("+-",p.nums)
    month = p.Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
    serverDateTime = p.Group(p.Suppress("[") + 
                             p.Combine(integer + "/" + month + "/" +
                                       integer + ":" + integer + ":" +
                                       integer + ":" + integer) +
                             timeZoneOffset + 
                             p.Suppress("]"))

    return ipAddress.setResultsName("ip_address") + \
           p.Suppress('-') + \
           p.Suppress('-') + \
           serverDateTime.setResultsName('datetime') + \
           p.dblQuotedString.setResultsName('cmd') \
               .setParseAction(getCmdFields) + \
           (integer | '-').setResultsName('status_code') + \
           (integer | '-').setResultsName('bytes_sent')  + \
           p.dblQuotedString.setResultsName('referrer') \
               .setParseAction(p.removeQuotes) + \
           p.dblQuotedString.setResultsName('user_agent') \
               .setParseAction(p.removeQuotes)

entry = partial(_entry, get_pyparser())

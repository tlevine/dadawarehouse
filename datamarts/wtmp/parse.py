import datetime

import pyparsing as p

twointeger = lambda name: p.Word(p.nums, exact = 2).setResultsName(name)
duration = p.Group(p.Suppress('(') +
                   twointeger('hours') +
                   p.Suppress(':') +
                   twointeger('minutes') +
                   p.Suppress(')')
           ).setResultsName('duration')

ip_address_byte = p.Word(p.nums, max = 3)
ip_address = p.Combine(ip_address_byte + '.' + ip_address_byte + '.' +
                       ip_address_byte + '.' + ip_address_byte)\
                .setResultsName('ip_address')

lastdatetime = p.Group(p.Word(p.alphas, exact=3).setResultsName('day_of_week') +
                       p.Word(p.alphas, exact=3).setResultsName('month') +
                       p.Word(p.nums, max = 2).setResultsName('day') +
                       twointeger('hour') + p.Suppress(':') +
                       twointeger('minute') + p.Suppress(':') +
                       twointeger('second') +
                       p.Word(p.nums, exact = 4).setResultsName('year'))

parser = p.Word(p.alphanums).setResultsName('user') + \
         p.Word(p.alphanums + '/').setResultsName('tty') + \
         lastdatetime.setResultsName('login_datetime') + \
         p.Suppress('-') + \
         lastdatetime.setResultsName('logout_datetime') + \
         duration + \
         ip_address + \
         p.restOfLine

def parse(line):
    DATEFORMAT = '%Y%b%d%H%M%S'
    result = dict(parser.parseString(line))
    del(result['duration'])
    for key in ['login_datetime', 'logout_datetime']:
        raw = result[key]
        datestring = raw.year + raw.month + raw.day + raw.hour + raw.minute + raw.second
        result[key] = datetime.datetime.strptime(datestring, DATEFORMAT)
    return result

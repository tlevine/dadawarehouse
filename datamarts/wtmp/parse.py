import pyparsing as p

twointeger = lambda name: p.Word(p.nums, exact = 2).setResultsName(name)
duration = p.Combine('(' + twointeger('hours') +
                     ':' + twointeger('minutes') + ')')\
               .setResultsName('duration')

ip_address_byte = p.Word(p.nums, max = 3)
ip_address = p.Combine(ip_address_byte + '.' + ip_address_byte + '.' +
                       ip_address_byte + '.' + ip_address_byte)\
                .setResultsName('ip_address')

datetime = p.Group(p.Word(p.alphas, exact=3).setResultsName('day_of_week') +
                   p.Word(p.alphas, exact=3).setResultsName('month') +
                   p.Word(p.nums + ' ', exact = 2).setResultsName('day') +
                   p.Combine(twointeger('hour') + ':' +
                             twointeger('minute') + ':' +
                             twointeger('second')) +
                   p.Word(p.nums, exact = 4).setResultsName('year'))

parser = p.Word(p.alphanums).setResultsName('user') + \
         p.Word(p.alphanums + '/').setResultsName('tty') + \
         datetime.setResultsName('login_datetime') + \
         p.Suppress('-') + \
         datetime.setResultsName('logout_datetime') + \
         duration + \
         ip_address + \
         p.restOfLine

line = 'tlevine  pts/7        Fri Aug  1 10:05:24 2014 - Fri Aug  1 10:15:07 2014  (00:09)     178.36.15.241 via mosh [30685]\n'
print(parser.parseString(line))

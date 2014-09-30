import string

import pyparsing as p

day_of_week = p.Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
month = p.Word(string.ascii_uppercase, string.ascii_lowercase, exact=3)
duration = p.Combine('(' + integer + ':' + integer + ')')
ip_address = p.Combine(integer + '.' + integer + '.' +
                       integer + '.' + integer + '.')

datetime = p.Group(day_of_week + 
                   month +
                   integer + 
                   p.Combine(integer + ':' + integer + ':' integer) +
                   integer)

parser = p.Word() + p.Word() +
         datetime +
         p.Suppress('-') +
         datetime +
         duration +
         ip_address + 
         p.restOfLine


line = 'tlevine  pts/7        Fri Aug  1 10:05:24 2014 - Fri Aug  1 10:15:07 2014  (00:09)     178.36.15.241 via mosh [30685]\n'
print(parser.parseString(line))

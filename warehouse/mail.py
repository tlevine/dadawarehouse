import os, email

DIR = '/home/tlevine/safe/maildir/cold/_@thomaslevine.com-2014-08-06/Archive/cur'
MAIL = '1404236989_3.11734.arch,U=5553,FMD5=e727b00944f81e1d0a95c12886ac4641:2,RS'

message = email.message_from_file(open(os.path.join(DIR, MAIL), 'r'))

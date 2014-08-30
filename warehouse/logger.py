import os
import logging

level = logging.DEBUG
filename = os.path.expanduser('~/.dadawarehouse/warehouse.log')
filename = None

logger = logging.getLogger('dadawarehouse')
logger.setLevel(level)

stream = logging.StreamHandler()
stream.setLevel(level)
logger.addHandler(stream)

logfile = logging.FileHandler(filename, 'a')
logfile.setLevel(level)
logger.addHandler(logfile)

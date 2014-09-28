from sqlalchemy.dialects.postgres import ARRAY

from doeund import Column

def Array(columntype):
    return Column(ARRAY(columntype, dimensions = 1))

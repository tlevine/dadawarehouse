from sqlalchemy.dialects.postgres import ARRAY

def Array(columntype):
    return Column(ARRAY(columntype, dimensions = 1))

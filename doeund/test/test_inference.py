from collections import namedtuple

from doeund.inference import fact_measures

Table = namedtuple('Table', ['columns'])
Column = namedtuple('Column', ['name', 'foreign_keys'])

def test_fact_measures():
    name = Column('name', set())
    height = Column('height', set())
    city = Column('city', {'Pretend this is a city column.'})
    table = Table([name, height, city])

    observed = fact_measures(table)
    expected = {'name': [name], 'height': [height]}

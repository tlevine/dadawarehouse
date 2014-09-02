from collections import namedtuple

import nose.tools as n

from doeund.inference import fact_measures

Table = namedtuple('Table', ['columns'])
Column = namedtuple('Column', ['name', 'foreign_keys'])

def test_fact_measures_fake():
    name = Column('name', set())
    height = Column('height', set())
    city = Column('city', {'Pretend this is a city column.'})
    table = Table([name, height, city])

    observed = fact_measures(table)
    expected = {'name': [name], 'height': [height]}
    n.assert_dict_equal(observed, expected)

def test_fact_measures_real():
    import warehouse.main
    cube = warehouse.main.query()['fact_calendarevent']

    observed = list(fact_measures(cube._args[1]).keys())
    expected = ['event_id', 'event_date', 'event_description']
    n.assert_list_equal(observed, expected)

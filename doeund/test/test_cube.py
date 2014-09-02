import nose.tools as n

import warehouse.main

cube = warehouse.main.query()['fact_calendarevent']

def test_fact_measures():
    n.assert_list_equal(list(cube.dimensions.keys()), ['calendarfile'])

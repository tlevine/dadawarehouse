import nose.tools as n

import warehouse.main

cube = warehouse.main.query()['fact_calendarevent']

def test_keys():
    n.assert_list_equal(cube.dimensions.keys(), ['calendarfile'])

import nose.tools as n

import warehouse.main

cube = warehouse.main.query()['fact_calendarevent']

def test_dimensions():
    observed = list(cube.dimensions.keys())
    expected = ['calendarfile', 'event_description']
    n.assert_list_equal(observed, expected)

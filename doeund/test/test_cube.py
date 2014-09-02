import nose.tools as n

import warehouse.main

cube = warehouse.main.query()['fact_calendarevent']

def test_dimensions():
    observed = list(cube.dimensions.keys())
    expected = ['event_id', 'event_date', 'event_description', 'calendarfile']
    n.assert_list_equal(observed, expected)

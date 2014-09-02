import nose.tools as n

from doeund.inference import fact_measures
import warehouse.main

cube = warehouse.main.query()['fact_calendarevent']

def test_fact_measures():
    observed = list(fact_measures(cube._args[1]).keys())
    expected = ['event_id', 'event_date', 'event_description']
    n.assert_list_equal(observed, expected)

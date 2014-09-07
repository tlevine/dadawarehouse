from functools import reduce

from .inference import dim_levels as _dim_levels, fact_measures as _fact_measures, joins as _joins

def export(tables):
    initial = {'dimensions':[], 'cubes': []}
    return reduce(add_table, tables.values(), initial)

def add_table(model, table):
    model = dict(model)
    if table.name.startswith('fact_'):
        model['cubes'].append(parse_fact_table(table))
    elif table.name.startswith('dim_'):
        model['dimensions'].append(parse_dim_table(table))
    else:
        warnings.warn('I\'m ignoring table "%s" because it is neither a fact nor a dimension.' % table.name)
    return model

def parse_fact_table(table):
    return {
        'name': table.name,
        'label': table.info.get('label', table.name),
        'dimensions': ["date_sale", "customer", "product", "country" ],
        'measures': list(fact_measures(table))
        'joins': list(joins(table)),
    #   'mappings': {},
    }

def parse_dim_table(table):
    levels = 
    hierarchies = 
    return {
        'name': table.name,
        'label': table.info.get('label', table.name),
        'levels': [{'name': , 'label': }],
        'hierarchies': [{'name': , 'label': , 'levels': []}],
    }

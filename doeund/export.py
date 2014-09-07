from functools import reduce

from .inference import dim_levels, fact_measures, joins, mappings

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
        'dimensions': list(dimensions(table)),
        'measures': list(fact_measures(table)),
        'joins': list(joins(table)),
        'mappings': dict(mappings(table)),
    }

def parse_dim_table(table):
    levels = dim_levels(table)
    return {
        'name': table.name,
        'label': table.info.get('label', table.name),
        'levels': levels,
        'hierarchies': [level['name'] for level in levels],
    }

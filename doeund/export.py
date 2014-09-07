from functools import reduce

def export(tables):
    initial = {'dimensions':[], 'cubes': []}
    return reduce(add_table, tables.values(), initial)

def add_table(model, table):
    if table.name.startswith('fact_'):
        f = add_fact_table
    elif table.name.startswith('dim_'):
        f = add_dim_table
    else:
        warnings.warn('I\'m ignoring table "%s" because it is neither a fact nor a dimension.' % table.name)
        f = lambda m: m
    return f(model, table)

def add_fact_table(model, table):
    pass

def add_dim_table(model, table):

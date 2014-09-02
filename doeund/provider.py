from cubes import ModelProvider as _ModelProvider

class _DoeundProvider(_ModelProvider):
    def __init__(self, metadata = None, declarative_base = None):
        super(Model, self).__init__(metadata)
        if declarantive_base == None:
            raise TypeError('declarative_base must be set.')
        else:
            self.Base = declarative_base

    def list_cubes(self):
    # return a list of cubes that the provider provides. Return value should be a dictionary with keys: name, label, description and info.
        for table_name, table in Base.metadata.tables.items():
            if table_name.startswith('fact_'):
                yield cube(table)

    def cube(self, name):
        '''
        return a cubes.Cube object
        given its short name
        '''
        return cube(Base.metadata.tables['fact_' + name])

    def dimension(self, name, dimensions):
    # return a cubes.Dimension object. dimensions is a dictionary of public dimensions that can be used as templates. If a template is missing the method should raise TemplateRequired(template) error.

def cube(table):



def dim_levels(table):
    '''
    Everything that isn't a primary key is a level.'
    '''
    return filter(lambda column: not column.primary_key, table.columns)

def fact_measures(table):
    '''
    List the columns that are not foreign keys.
    '''
    return filter(lambda column: len(column.foreign_keys) == 0, table.columns)

def fact_joins(table):
    '''
    List the joins from this fact table to dimension tables.
    yields (column in this table, column in the other table)
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            # foreign_key.target_fullname
            yield column, foreign_key.column

def fact_dimensions(table):
    '''
    List this fact table's dimension tables.
    (tables that this table joins to)
    '''
    for column in table.columns:
        for foreign_key in column.foreign_keys:
            yield foreign_key.column.table

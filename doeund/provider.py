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

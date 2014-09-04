def d(function):
    'Make a "default" function.'
    def default(context):
        return function(context.current_parameters['pk'])
    return default

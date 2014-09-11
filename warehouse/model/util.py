def d(function):
    'Make a "default" function.'
    def default(context):
        try:
            return function(context.current_parameters['pk'])
        except:
            print(dict(context.current_parameters))
            raise
    return default

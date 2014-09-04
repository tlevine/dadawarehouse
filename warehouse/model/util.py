def d(function):
    'Make a "default" function.'
    def func(context):
        return function(context.current_parameters['pk'])

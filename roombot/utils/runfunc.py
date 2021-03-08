import inspect


async def run_func_as_async(function, *func_args, **func_kwargs):
    if inspect.iscoroutinefunction(function):
        return await function(*func_args, **func_kwargs)
    else:
        return function(*func_args, **func_kwargs)


def get_kwargs_by_annotations(function, arguments):
    params = list(inspect.signature(function).parameters.items())
    func_args = {}
    num = 0
    for param in params:
        if num >= len(arguments):
            break
        _, parameter = param
        func_args[parameter.name] = arguments.get(parameter.annotation)
        if not func_args[parameter.name]:
            pass
        num += 1
    return func_args


def get_only_the_required_arguments(function, arguments):
    params = list(inspect.signature(function).parameters.items())
    func_args = {}
    for param in params:
        _, parameter = param
        if parameter.name in arguments:
            func_args[parameter.name] = arguments.get(parameter.name)
    return func_args


def notImplementedYet(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f'{func.__name__} is not implemented yet')

    return wrapper

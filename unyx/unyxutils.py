def notImplementedYet(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f'{func.__name__} is not implemented yet')

    return wrapper


def notDone(func):
    def wrapper(*args, **kwargs):
        print(f'{func.__name__} is not done yet')
        func(*args, **kwargs)

    return wrapper

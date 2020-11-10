class CursedUIException(Exception):
    '''
    CursedUI exception base class.
    Avoid raising it directly (use subclasses).
    '''
    pass


class DecoratorException(CursedUIException):
    '''
    Decorators exception
    '''
    pass

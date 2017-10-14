import functools
import logging


class Log:
    FORMAT_LOG = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"

    def __init__(self):
        self.log = logging.getLogger(__name__)
        logging.basicConfig(format=Log.FORMAT_LOG)
        self.log.setLevel(logging.DEBUG)

    def get_log(self):
        return self.log


def singleton(cls):
    ''' Use class as singleton. '''

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


#
# Sample use:
#
# @singleton
# class __Foo:
#     def __new__(cls):
#         cls.x = 10
#         return object.__new__(cls)
#
#     def __init__(self):
#         assert self.x == 10
#         self.x = 15
#
#
# assert __Foo().x == 15
# __Foo().x = 20
# assert __Foo().x == 20

class log_entry(object):
    '''Logging decorator that allows you to log with a specific logger.'''
    # Customize these messages
    ENTRY_MESSAGE = 'Entering [{}]'
    EXIT_MESSAGE = 'Exiting [{}]'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        ''' Returns a wrapper that wraps func.
            The wrapper will log the entry and exit points of the function
            with logging.INFO level.
        '''
        # set logger if it was not set earlier
        if not self.logger:
            self.logger = Log().get_log()

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            # logging level .info(). Set to .debug() if you want to
            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))

            # Execute function
            f_result = func(*args, **kwds)

            # logging level .info(). Set to .debug() if you want to
            self.logger.info(self.EXIT_MESSAGE.format(func.__name__))

            return f_result

        return wrapper

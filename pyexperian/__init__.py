import logging
__version__ = '1.0.2'


def enable_debug(filename='pyexperian.log'):
    import datetime
    print('Debug mode is on. Events are logged at: %s' % filename)
    logging.basicConfig(filename=filename, level=logging.INFO)
    logging.info('\nLogging session starts: %s' % (str(datetime.datetime.today())))


def disable_debug():
    logging.basicConfig(level=logging.WARNING)
    print('Debug mode is off.')


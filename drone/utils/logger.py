from drone.config.settings import logger


def write_log(msg=None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            if msg:
                logger.debug(msg)
            logger.debug('%s %s %s' % (str(f), str(args), str(kwargs)))
            result = f(*args, **kwargs)
            logger.debug(result)
            return result

        return wrapped_f

    return wrap

def __init_logger():
    import logging
    logger = logging.getLogger('pytools')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] -> [%(filename)s: '
        '%(funcName)s] -> [%(levelname)s]: %(message)s')
    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

logger = __init_logger()

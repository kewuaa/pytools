import logging


def __init_logger():
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


__logger = __init_logger()
__info_logger = None
__warning_logger = None
__error_logger = None


def add_info_logger(logger):
    assert callable(logger)
    global __info_logger
    __info_logger = logger


def add_warning_logger(logger):
    assert callable(logger)
    global __warning_logger
    __warning_logger = logger


def add_error_logger(logger):
    assert callable(logger)
    global __error_logger
    __error_logger = logger


def info(msg: str) -> None:
    __logger.info(msg)
    if __info_logger is not None:
        __info_logger(msg)


def warning(msg: str) -> None:
    __logger.warning(msg)
    if __warning_logger is not None:
        __warning_logger(msg)


def error(msg: str) -> None:
    __logger.error(msg)
    if __error_logger is not None:
        __error_logger(msg)

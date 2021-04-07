import logging

from queue import Queue
from enum import IntEnum
from logging.handlers import QueueHandler

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"


class LoggingLevel(IntEnum):
    NOTSET = 0
    DEBUG = 10
    USER_DEBUG = 15,
    INFO = 20
    USER_INFO = 25,
    WARNING = 30
    USER_WARNING = 35,
    ERROR = 40
    USER_ERROR = 45
    CRITICAL = 50


class IngeniaAdapter(logging.LoggerAdapter):
    custom_fields = ["axis", "drive", "code_error"]

    def user_debug(self, msg, *args, **kwargs):
        self.log(LoggingLevel.USER_DEBUG, msg, *args, **kwargs)

    def user_info(self, msg, *args, **kwargs):
        self.log(LoggingLevel.USER_INFO, msg, *args, **kwargs)

    def user_warning(self, msg, *args, **kwargs):
        self.log(LoggingLevel.USER_WARNING, msg, *args, **kwargs)

    def user_error(self, msg, *args, **kwargs):
        self.log(LoggingLevel.USER_ERROR, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        extra_list = []
        for field_name in self.custom_fields:
            field_value = kwargs.pop(field_name, self.extra.get(field_name))
            if field_value is not None:
                extra_list.append('{}="{}"'.format(field_name, field_value))
        extra_str = ""
        if extra_list:
            extra_str = "({}) ".format(", ".join(extra_list))
        return '%s%s' % (extra_str, msg), kwargs


def configure_logger(level=logging.WARNING, queue=False, file=None):
    """
    Do Ingenia configuration for the logging system. By default configure a StreamHandler, but can configure a
    QueueHandler and FileHandler.

    Args:
        level (int): set the root logger level to the specified level. ``logging.WARNING`` by default.
        queue (bool): if ``True``, configure a QueueHandler and return the queue, if ``False`` do nothing.
         ``False`` by default.
        file (str): if set, configure a FileHandler with this param as filename. ``None`` by default.

    Returns:
        queue.Queue or None: if queue is ``True`` return the queue, if it is ``False`` return ``None``.
    """
    logging.addLevelName(LoggingLevel.USER_DEBUG, LoggingLevel.USER_DEBUG.name)
    logging.addLevelName(LoggingLevel.USER_INFO, LoggingLevel.USER_INFO.name)
    logging.addLevelName(LoggingLevel.USER_WARNING, LoggingLevel.USER_WARNING.name)
    logging.addLevelName(LoggingLevel.USER_ERROR, LoggingLevel.USER_ERROR.name)

    root_logger = logging.getLogger()
    formatter = logging.Formatter(FORMAT)
    root_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if file:
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    if queue:
        log_queue = Queue()
        queue_handler = QueueHandler(log_queue)
        queue_handler.setFormatter(formatter)
        root_logger.addHandler(queue_handler)
        return log_queue


def get_logger(name, axis=None, drive=None, code_error=None):
    """
    Return logger with target name.

    Args:
        name (str): logger name.
        axis (int): default value for logger axis. ``None`` as a default.
        drive (str): default value for logger drive. ``None`` as a default.
        code_error (str): default value for logger drive. ``None`` as a default.

    Returns:
        logging.LoggerAdapter: return logger

    """
    logger = logging.getLogger(name)
    extra = {
        "axis": axis,
        "drive": drive,
        "code_error": code_error
    }
    return IngeniaAdapter(logger, extra)

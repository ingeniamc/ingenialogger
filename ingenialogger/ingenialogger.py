import logging

from queue import Queue
from enum import IntEnum
from logging.handlers import QueueHandler

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"


class LoggingLevel(IntEnum):
    NOTSET = 0
    DEBUG = 10
    PUBLIC_DEBUG = 15
    INFO = 20
    PUBLIC_INFO = 25
    WARNING = 30
    PUBLIC_WARNING = 35
    ERROR = 40
    PUBLIC_FAULT = 43
    PUBLIC_ERROR = 45
    CRITICAL = 50


class IngeniaAdapter(logging.LoggerAdapter):
    custom_fields = ["axis", "drive", "category", "code_error"]

    def public_debug(self, msg, *args, **kwargs):
        self.log(LoggingLevel.PUBLIC_DEBUG, msg, *args, **kwargs)

    def public_info(self, msg, *args, **kwargs):
        self.log(LoggingLevel.PUBLIC_INFO, msg, *args, **kwargs)

    def public_warning(self, msg, *args, **kwargs):
        self.log(LoggingLevel.PUBLIC_WARNING, msg, *args, **kwargs)

    def public_error(self, msg, *args, **kwargs):
        self.log(LoggingLevel.PUBLIC_ERROR, msg, *args, **kwargs)

    def public_fault(self, msg, *args, **kwargs):
        self.log(LoggingLevel.PUBLIC_FAULT, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        extra_list = []
        for field_name in self.custom_fields:
            field_value = kwargs.pop(field_name, self.extra.get(field_name))
            if field_value is not None:
                extra_list.append('{}="{}"'.format(field_name, field_value))
        extra_str = ""
        if extra_list:
            extra_str = "({}) ".format(", ".join(extra_list))
        return "%s%s" % (extra_str, msg), kwargs


class IngeniaHandlers:
    steam_handler = None
    queue_handler = None
    file_handler = None


def check_logger_handler(logger, handler):
    id_list = [id(x) for x in logger.handlers]
    return id(handler) in id_list


ingenia_handlers = IngeniaHandlers()


def configure_logger(level=logging.WARNING):
    """
    Do Ingenia configuration for the logging system. By default configure a StreamHandler.

    Args:
        level (int): set the root logger level to the specified level. ``logging.WARNING`` by default.
    """
    logging.addLevelName(LoggingLevel.PUBLIC_DEBUG, LoggingLevel.PUBLIC_DEBUG.name)
    logging.addLevelName(LoggingLevel.PUBLIC_INFO, LoggingLevel.PUBLIC_INFO.name)
    logging.addLevelName(LoggingLevel.PUBLIC_WARNING, LoggingLevel.PUBLIC_WARNING.name)
    logging.addLevelName(LoggingLevel.PUBLIC_ERROR, LoggingLevel.PUBLIC_ERROR.name)
    logging.addLevelName(LoggingLevel.PUBLIC_FAULT, LoggingLevel.PUBLIC_FAULT.name)

    root_logger = logging.getLogger()
    formatter = logging.Formatter(FORMAT)
    root_logger.setLevel(level)

    if ingenia_handlers.steam_handler is None:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        ingenia_handlers.steam_handler = console_handler
    if not check_logger_handler(root_logger, ingenia_handlers.steam_handler):
        root_logger.addHandler(ingenia_handlers.steam_handler)


def configure_file_handler(filename):
    """Configure a FileHandler.

    Args:
        filename: Path to the file where the log will be stored.
    """

    root_logger = logging.getLogger()
    formatter = logging.Formatter(FORMAT)
    print(ingenia_handlers)
    if ingenia_handlers.file_handler is None:
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)
        ingenia_handlers.file_handler = file_handler
    if not check_logger_handler(root_logger, ingenia_handlers.file_handler):
        root_logger.addHandler(ingenia_handlers.file_handler)


def configure_queue_handler():
    """Configure a QueueHandler.

    Returns:
        queue.Queue: Log queue.
    """

    root_logger = logging.getLogger()
    formatter = logging.Formatter(FORMAT)

    if ingenia_handlers.queue_handler is None:
        log_queue = Queue()
        queue_handler = QueueHandler(log_queue)
        queue_handler.setFormatter(formatter)
        ingenia_handlers.queue_handler = queue_handler
    if not check_logger_handler(root_logger, ingenia_handlers.queue_handler):
        root_logger.addHandler(ingenia_handlers.queue_handler)
    return ingenia_handlers.queue_handler.queue


def clean_ingenia_handlers():
    """Clean ingenia handlers."""
    global ingenia_handlers
    ingenia_handlers = IngeniaHandlers()


def get_logger(name, axis=None, drive=None, category=None, code_error=None):
    """
    Return logger with target name.

    Args:
        name (str): logger name.
        axis (int): default value for logger axis. ``None`` as a default.
        drive (str): default value for logger drive. ``None`` as a default.
        category (str): default value for error type. ``None`` as default.
        code_error (str): default value for error identifier. ``None`` as a default.

    Returns:
        IngeniaAdapter: return logger

    """
    logger = logging.getLogger(name)
    extra = {"axis": axis, "drive": drive, "category": category, "code_error": code_error}
    return IngeniaAdapter(logger, extra)

import logging

from queue import Queue
from logging.handlers import QueueHandler

FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
logger_dict = {}


class IngeniaAdapter(logging.LoggerAdapter):
    custom_fields = ["axis", "drive", "code_error"]

    def process(self, msg, kwargs):
        extra_list = []
        for field_name in self.custom_fields:
            field_value = kwargs.pop(field_name, None)
            if field_value:
                extra_list.append('{}="{}"'.format(field_name, field_value))
        extra_str = ""
        if extra_list:
            extra_str = "({}) ".format(", ".join(extra_list))
        return '%s%s' % (extra_str, msg), kwargs


def configure_logging(level=logging.WARNING, queue=False, file=None):
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


def get_logger(name):
    """
    Return logger with target name.

    Args:
        name: logger name.

    Returns:
        logging.LoggerAdapter: return logger

    """
    logger = logging.getLogger(name)
    if name not in logger_dict:
        logger_dict[name] = IngeniaAdapter(logger, {})
    return logger_dict[name]

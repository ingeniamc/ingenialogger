__version__ = '0.2.0'
""" str: Library version. """
from .ingenialogger import (
    get_logger,
    configure_logger,
    configure_file_handler,
    configure_queue_handler, 
    clean_ingenia_handlers,
    LoggingLevel
)
from .parser import LogParser
__all__ = [
    "get_logger",
    "configure_logger",
    "configure_file_handler",
    "configure_queue_handler",
    "clean_ingenia_handlers",
    "LogParser",
    "LoggingLevel"
]

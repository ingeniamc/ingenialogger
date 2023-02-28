__version__ = '0.2.1'
""" str: Library version. """
from .ingenialogger import get_logger, configure_logger, LoggingLevel
from .parser import LogParser
__all__ = ["get_logger", "configure_logger", "LogParser", "LoggingLevel"]

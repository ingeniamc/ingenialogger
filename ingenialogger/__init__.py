__version__ = '0.1.0'
""" str: Library version. """
from .ingenialogger import get_logger, configure_logging
from .parser import LogParser
__all__ = ["get_logger", "configure_logging", "LogParser"]

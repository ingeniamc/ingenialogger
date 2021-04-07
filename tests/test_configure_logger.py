import pytest
import logging

from logging.handlers import QueueHandler

from ingenialogger import configure_logger, LoggingLevel


def test_configure_logger_handler_creation():
    root_logger = logging.getLogger()
    offset = len(root_logger.handlers)

    configure_logger(level=logging.INFO)
    assert len(root_logger.handlers) == offset + 1
    assert isinstance(root_logger.handlers[-1], logging.StreamHandler)

    configure_logger(level=logging.INFO, queue=True)
    assert len(root_logger.handlers) == offset + 2
    assert isinstance(root_logger.handlers[-1], QueueHandler)

    configure_logger(level=logging.INFO, file="temp")
    assert len(root_logger.handlers) == offset + 3
    assert isinstance(root_logger.handlers[-1], logging.FileHandler)

    configure_logger(level=logging.INFO)
    assert len(root_logger.handlers) == offset + 3
    assert isinstance(root_logger.handlers[-1], logging.StreamHandler)
    assert isinstance(root_logger.handlers[-2], QueueHandler)
    assert isinstance(root_logger.handlers[-3], logging.StreamHandler)


def test_configure_logger_queue():
    root_logger = logging.getLogger("test")

    log_queue = configure_logger(level=logging.INFO, queue=True)
    root_logger.info("log 1")
    msg_1 = log_queue.get(block=False)
    assert msg_1.msg == "log 1"

    log_queue = configure_logger(level=logging.INFO, queue=True)
    root_logger.info("log 2")
    msg_2 = log_queue.get(block=False)
    assert msg_2.msg == "log 2"

    configure_logger(level=logging.INFO, queue=True)
    root_logger.info("log 3")
    msg_3 = log_queue.get(block=False)
    assert msg_3.msg == "log 3"


@pytest.mark.parametrize("level", [LoggingLevel.DEBUG,
                                   LoggingLevel.USER_DEBUG,
                                   LoggingLevel.INFO,
                                   LoggingLevel.USER_INFO,
                                   LoggingLevel.WARNING,
                                   LoggingLevel.USER_WARNING,
                                   LoggingLevel.ERROR,
                                   LoggingLevel.USER_ERROR,
                                   LoggingLevel.CRITICAL])
def test_configure_logger_levels(caplog, level):
    root_logger = logging.getLogger("test")
    configure_logger(level=logging.NOTSET)
    root_logger.log(level, "test")
    assert caplog.records.pop().levelname == level.name

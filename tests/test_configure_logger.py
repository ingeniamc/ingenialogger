import os
import logging
from logging.handlers import QueueHandler

import pytest

from ingenialogger import configure_logger, LoggingLevel
from ingenialogger import configure_file_handler, configure_queue_handler


def test_configure_logger():
    root_logger = logging.getLogger()
    offset = len(root_logger.handlers)

    configure_logger(level=logging.INFO)
    assert len(root_logger.handlers) == offset + 1
    assert isinstance(root_logger.handlers[-1], logging.StreamHandler)

    configure_logger(level=logging.INFO)
    configure_queue_handler()
    assert len(root_logger.handlers) == offset + 2
    assert isinstance(root_logger.handlers[-1], QueueHandler)

    configure_logger(level=logging.INFO)
    configure_file_handler("temp")
    assert len(root_logger.handlers) == offset + 3
    assert isinstance(root_logger.handlers[-1], logging.FileHandler)

    configure_logger(level=logging.INFO)
    assert len(root_logger.handlers) == offset + 3
    assert isinstance(root_logger.handlers[-1], logging.StreamHandler)
    assert isinstance(root_logger.handlers[-2], QueueHandler)
    assert isinstance(root_logger.handlers[-3], logging.StreamHandler)


def test_configure_queue_handler():
    root_logger = logging.getLogger("test")

    configure_logger(level=logging.INFO)
    log_queue = configure_queue_handler()
    root_logger.info("log 1")
    msg_1 = log_queue.get(block=False)
    assert msg_1.msg == "log 1"

    configure_logger(level=logging.INFO)
    log_queue = configure_queue_handler()
    root_logger.info("log 2")
    msg_2 = log_queue.get(block=False)
    assert msg_2.msg == "log 2"

    configure_logger(level=logging.INFO)
    log_queue = configure_queue_handler()
    root_logger.info("log 3")
    msg_3 = log_queue.get(block=False)
    assert msg_3.msg == "log 3"


def test_configure_file_handler():
    root_logger = logging.getLogger("test")
    filename = "test.log"

    if os.path.exists(filename):
        os.remove(filename)

    configure_logger(level=logging.INFO)
    configure_file_handler(filename)

    root_logger.info("log")
    assert os.path.exists(filename)

    with open(filename, "r") as log_file:
        log_lines = log_file.readlines()
    assert len(log_lines) == 1


@pytest.mark.parametrize(
    "level",
    [
        LoggingLevel.DEBUG,
        LoggingLevel.PUBLIC_DEBUG,
        LoggingLevel.INFO,
        LoggingLevel.PUBLIC_INFO,
        LoggingLevel.WARNING,
        LoggingLevel.PUBLIC_WARNING,
        LoggingLevel.ERROR,
        LoggingLevel.PUBLIC_FAULT,
        LoggingLevel.PUBLIC_ERROR,
        LoggingLevel.CRITICAL,
    ],
)
def test_configure_logger_levels(caplog, level):
    root_logger = logging.getLogger("test")
    configure_logger(level=logging.NOTSET)
    root_logger.log(level, "test")
    assert caplog.records.pop().levelname == level.name

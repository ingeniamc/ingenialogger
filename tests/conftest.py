import pytest
import logging

from importlib import reload

import ingenialogger


@pytest.fixture(scope="function", autouse=True)
def reset_logging():
    yield
    logger = logging.getLogger()
    logger.handlers = []
    reload(ingenialogger)
    ingenialogger.clean_ingenia_handlers()

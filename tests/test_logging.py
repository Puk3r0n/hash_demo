import pytest
from loguru import logger
import os


def test_logging_setup():
    log_message = "This is a test log message"
    log_file_path = "test.log"

    logger.add(log_file_path)

    logger.info(log_message)

    assert os.path.isfile(log_file_path)

    log_contents = open(log_file_path).read()
    assert log_message in log_contents

    os.remove(log_file_path)


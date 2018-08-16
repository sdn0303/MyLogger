# -*- Coding: UTF-8 -*-
from logger import Logger

# Set logger
LOGGER = Logger(__name__)


class TestClass(object):

    @Logger.cls_logger
    def test_func(self, x, y):
        return x * y - 100

    def raise_error(self):
        raise ZeroDivisionError


if __name__ == "__main__":
    t = TestClass()
    t.test_func(30, 50)

    LOGGER.info("information")
    LOGGER.debug("Start debug")
    try:
        LOGGER.warn("raise Exception")
        t.raise_error()
    except ZeroDivisionError:
        LOGGER.error("Division by Zero")
        LOGGER.critical("Division by Zero")

# -*- Coding: UTF-8 -*-
from logger import Logger

# Set logger
LOGGER = Logger.get_logger(__name__)


class TestClass(object):

    def test_func(self, x, y):
        return x * y - 100

    @Logger.time_measure(LOGGER, __file__)
    def test_time(self, x, y):
        return [i for i in range(x * y)]

    def raise_error(self):
        raise ZeroDivisionError


if __name__ == "__main__":
    t = TestClass()
    t.test_func(30, 50)

    LOGGER.info("information")
    LOGGER.debug("Start debug")
    try:
        LOGGER.warn("raise Exception")
        LOGGER.warning("Warning!! raise Exception")
        t.raise_error()
    except ZeroDivisionError:
        LOGGER.error("Division by Zero")
        LOGGER.critical("Division by Zero")

    t.test_time(100, 100)

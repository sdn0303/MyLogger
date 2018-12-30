# -*- Coding: UTF-8 -*-
import time
import logging
import sys
from datetime import datetime

from termcolor import colored
from colorama import Back, Fore, Style

# Set Str Date
STR_DATE = datetime.now().strftime("%Y-%m-%d %H:%M")


class Logger(object):
    COLOR_MAP = {
        'debug': Fore.CYAN,
        'info': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'critical': Back.RED,
    }

    def __init__(self, name):
        self.logger = self.app_logger(name)

    def __getattr__(self, attr_name):
        if attr_name == 'warn':
            attr_name = 'warning'
        if attr_name not in 'debug info warning error critical':
            return getattr(self.logger, attr_name)
        log_level = getattr(logging, attr_name.upper())
        if not self.logger.isEnabledFor(log_level):
            return

        def wrapped_attr(msg, *args, **kwargs):
            style_prefix = self.COLOR_MAP[attr_name]
            msg = style_prefix + msg + Style.RESET_ALL
            return self.logger._log(log_level, msg, args, **kwargs)

        return wrapped_attr

    @staticmethod
    def app_logger(name) -> object():
        """ アプリケーションロガー

        Args:
            name: 実行ファイル名

        Returns:
            object(): logger
        """
        logger = logging.getLogger(name)
        stream_handler = logging.StreamHandler()
        fmt = "{} [{}] [{}:{}] [%(levelname)s] %(message)s".format(
            colored('%(asctime)s', "magenta", attrs=['reverse']),
            colored('%(threadName)s', "green"),
            colored('%(filename)s', "cyan", attrs=['bold']),
            colored('%(lineno)d', "cyan", attrs=['bold']))

        if stream_handler:
            logging.basicConfig(
                stream=sys.stderr,
                level=logging.INFO,
                format=fmt)
        return logger

    def time_measure(self, func):
        """ 関数の実行時間計測メソッド

        Args:
            func: 各クラスのメソッド

        Returns:
            object(): wrapperメソッドの実行結果
        """
        def wrapper(obj, *args, **kwargs):
            start = time.time()
            self.logger.info('Measure execution time.')
            self.logger.info('func: {}'.format(func.__qualname__))
            r = func(obj, *args, **kwargs)
            end = time.time() - start
            m, s = divmod(end, 60)
            self.logger.info("Elapsed time:{0} [sec]".format(s))
            self.logger.info("Elapsed time:{0} [min]".format(m))
            return r
        return wrapper

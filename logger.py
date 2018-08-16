# -*- Coding: UTF-8 -*-
from datetime import datetime
import logging
import sys

from termcolor import colored
from colorama import Back, Fore, Style


# Set Str Date
STR_DATE = datetime.now().strftime("%Y-%m-%d %H:%M")


class Logger(object):
    """ ロガークラス"""
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
            colored('pid:%(process)s', "green"),
            colored('%(filename)s', "cyan", attrs=['bold']),
            colored('%(lineno)d', "cyan", attrs=['bold']))

        if stream_handler:
            logging.basicConfig(
                stream=sys.stderr,
                level=logging.DEBUG,
                format=fmt)
        return logger

    @staticmethod
    def cls_logger(func: object()) -> object():
        """ 各クラスメソッド用ロギングデコレーター\n
        処理開始時にメソッドが保持しているパラメーターと処理後の結果を出力する

        Args:
            func: 各クラスのメソッド

        Returns:
            object(): wrapperメソッドの実行結果
        """
        def wrapper(obj, *args, **kwargs) -> object():
            print("{} [Func: {}] [Input] [args={}] [kwargs={}]".format(
                colored(STR_DATE, "blue", attrs=['reverse']),
                colored(func.__qualname__, "cyan", attrs=['bold']),
                colored(args, "yellow"),
                colored(kwargs, "yellow")))

            rtn = func(obj, *args, **kwargs)
            print("{} [Func: {}] [Output] [return: {}]".format(
                colored(STR_DATE, "blue", attrs=['reverse']),
                colored(func.__qualname__, "cyan", attrs=['bold']),
                colored(rtn, "green")), end='\n\n')
            return rtn
        return wrapper

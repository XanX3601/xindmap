import kivy.logger as klogger
import logging

message_format = '{}: '

def critical(message, *args):
    """logs a critical message

    Args:
        message: the message to log
        args: the arguments to format into the message
    """
    if klogger.Logger.isEnabledFor(logging.CRITICAL):
        klogger.Logger.critical(message.format(*args))

def debug(message, *args):
    """logs a debug message

    Args:
        message: the message to log
        args: the arguments to format into the message
    """
    if klogger.Logger.isEnabledFor(logging.DEBUG):
        klogger.Logger.debug(message.format(*args))

def info(message, *args):
    """logs an info message

    Args:
        message: the message to log
        args: the arguments to format into the message
    """
    if klogger.Logger.isEnabledFor(logging.INFO):
        klogger.Logger.info(message.format(*args))

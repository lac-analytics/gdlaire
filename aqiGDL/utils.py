"""General utility functions."""
import datetime as dt
from . import settings
import logging as lg
import unicodedata
import os


def ts(style="datetime", template=None):
    """
    Get current timestamp as string.
    Parameters
    ----------
    style : string
        format the timestamp with this built-in template. must be one
        of {'datetime', 'date', 'time'}
    template : string
        if not None, format the timestamp with this template instead of
        one of the built-in styles
    Returns
    -------
    ts : string
        the string timestamp
    """
    if template is None:
        if style == "datetime":
            template = "{:%Y-%m-%d %H:%M:%S}"
        elif style == "date":
            template = "{:%Y-%m-%d}"
        elif style == "time":
            template = "{:%H:%M:%S}"
        else:
            raise ValueError(f'unrecognized timestamp style "{style}"')

    ts = template.format(dt.datetime.now())
    return ts


# Logger functions taken from OSMnx
def log(message, level=None, name=None, filename=None):
    """
    Write a message to the logger.
    This logs to file and/or prints to the console (terminal), depending on
    the current configuration of settings.log_file and settings.log_console.
    Parameters
    ----------
    message : string
        the message to log
    level : int
        one of the logger.level constants
    name : string
        name of the logger
    filename : string
        name of the log file
    Returns
    -------
    None
    """
    if level is None:
        level = settings.log_level
    if name is None:
        name = settings.log_name
    if filename is None:
        filename = settings.log_filename

    logger = _get_logger(level=level, name=name, filename=filename)
    if level == lg.DEBUG:
        logger.debug(message)
    elif level == lg.INFO:
        logger.info(message)
    elif level == lg.WARNING:
        logger.warning(message)
    elif level == lg.ERROR:
        logger.error(message)


def _get_logger(level=None, name=None, filename=None):
    """
    Create a logger or return the current one if already instantiated.
    Parameters
    ----------
    level : int
        one of the logger.level constants
    name : string
        name of the logger
    filename : string
        name of the log file
    Returns
    -------
    logger : logging.logger
    """
    if level is None:
        level = settings.log_level
    if name is None:
        name = settings.log_name
    if filename is None:
        filename = settings.log_filename

    logger = lg.getLogger(name)

    # if a logger with this name is not already set up
    if not getattr(logger, "handler_set", None):

        # get today's date and construct a log filename
        log_filename = os.path.join(
            settings.logs_folder, f'{filename}_{ts(style="date")}.log')

        # if the logs folder does not already exist, create it
        if not os.path.exists(settings.logs_folder):
            os.makedirs(settings.logs_folder)

        # create file handler and log formatter and set them up
        handler = lg.FileHandler(log_filename, encoding="utf-8")
        formatter = lg.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.handler_set = True

    return logger

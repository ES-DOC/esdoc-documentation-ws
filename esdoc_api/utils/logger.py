# -*- coding: utf-8 -*-
"""
.. module:: utils.logger.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Logging utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime as dt



# Set of logging levels.
LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'
LOG_LEVEL_FATAL = 'FATAL'
LOG_LEVEL_SECURITY = 'SECURITY'

# Defaults.
_DEFAULT_MODULE = "**"

# Text to display when passed a null message.
_NULL_MSG = "-------------------------------------------------------------------------------"


def _get_formatted_message(msg, module, level):
    """Returns a message formatted for logging.

    """
    if msg is None:
        return _NULL_MSG

    return "{} [{}] :: ES-DOC > {} : {}".format(
        dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        level,
        module,
        str(msg).strip()
        )


def log(msg=None, module=_DEFAULT_MODULE, level=LOG_LEVEL_INFO):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str module: Module emitting log message (e.g. MQ).
    :param str level: Message level (e.g. INFO).

    """
    # TODO use structlog rather than printing to stdout
    print(_get_formatted_message(msg, module, level))


def log_error(err, module=_DEFAULT_MODULE):
    """Logs a runtime error.

    :param Exception err: Error to be written to log.
    :param str module: Module emitting log message (e.g. DB).

    """
    msg = "!! {0} RUNTIME ERROR !! :: ".format(module)
    if issubclass(BaseException, err.__class__):
        msg += "{} :: ".format(err.__class__)
    msg += "{}".format(err)
    log(msg, module, LOG_LEVEL_ERROR)


def log_db(msg, level=LOG_LEVEL_INFO):
    """Logs database related events.

    :param str msg: Database message for writing to log.
    :param str level: Message level (e.g. INFO).

    """
    log(msg, "DB", level)


def log_db_warning(msg):
    """Logs a database warning event.

    :param str msg: A log message.
    :param str level: Message level (e.g. INFO).

    """
    log_db(msg, level=LOG_LEVEL_WARNING)


def log_db_error(err):
    """Logs a database error event.

    :param Exception err: Exception to be logged.

    """
    log_error(err, "DB")


def log_web(msg, level=LOG_LEVEL_INFO):
    """Logs web related events.

    :param str msg: A log message.
    :param str level: Message level (e.g. INFO).

    """
    log(msg, "WEB", level)


def log_web_warning(msg):
    """Logs a web warning event.

    :param str msg: A log message.

    """
    log_web(msg, LOG_LEVEL_WARNING)


def log_web_security(msg):
    """Logs a web security event.

    :param str msg: A log message.

    """
    log_web(msg, LOG_LEVEL_SECURITY)


def log_web_error(err):
    """Logs a web error event.

    :param Exception err: Exception to be logged.

    """
    log_error(err, "WEB")

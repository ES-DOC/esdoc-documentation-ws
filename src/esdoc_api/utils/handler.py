"""
.. module:: utils.handler.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Web request handler utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: utf-8 -*-

# Module imports.
from . import (
    config,
    convert,
    runtime as rt
    )



# HTTP header names.
HTTP_HEADER_Access_Control_Allow_Origin = "Access-Control-Allow-Origin"


def _write_error(handler, error):
    """Writes an error response."""
    handler.clear()
    handler.write({
        'status': 1,
        'errorType': unicode(type(error)),
        'error': unicode(error)
        })


def _get_mime_type(encoding):
    """Maps and returns an encoding to an HTTP mime type."""
    encoding = encoding.lower()
    if encoding in ('csv', 'json', 'xml'):
        return 'application/{0}; charset=utf-8'.format(encoding)
    elif encoding == 'html':
        return 'text/html; charset=utf-8'
    elif encoding == 'jsonp':
        encoding = 'text/javascript; charset=utf-8'
    else:
        raise ValueError("Unknown encoding: {0}".format(encoding))


def _set_response_content(handler, encoding):
    """Sets response content."""
    # Get raw content.
    content = None if not hasattr(handler, 'output') else \
              getattr(handler, 'output')

    # Write html/csv/xml.
    if encoding in ('csv', 'html', 'xml'):
        content = content.strip() if content else ""

    # Write json/json-p.
    elif encoding == 'json':
        content = content if content else {}
        if 'status' not in content:
            content['status'] = 0
        if hasattr(handler, 'on_jsonp_load') and handler.on_jsonp_load:
            content = "{0}({1});".format(handler.on_jsonp_load, content)

    # Write.
    handler.write(content)


def _write(handler):
    """Writes a response."""
    # Derive content type.
    encoding = 'json' if not hasattr(handler, 'output_encoding') else \
               getattr(handler, 'output_encoding')
    encoding = encoding.lower()

    # Set HTTP response header.
    handler.set_header('Content-Type', _get_mime_type(encoding))

    # Set HTTP response content.
    _set_response_content(handler, encoding)


def _log(handler, error=None):
    """Logging utilty function."""
    if error:
        msg = "API --> error --> {0} --> {1}"
        msg = msg.format(handler, error)
        rt.log_api_error(msg)
    else:
        msg = "API --> success --> {0}"
        msg = msg.format(handler)
        rt.log_api(msg)


def _get_tasks(tasks):
    """Returns a set of tasks for execution."""
    if tasks is None:
        return ()
    try:
        iter(tasks)
    except TypeError:
        return (tasks, )
    else:
        return tasks


def invoke(handler, tasks=None, error_tasks=None):
    """Invokes a set of handler tasks and handles errors.

    :param tasks: A set of tasks.
    :type tasks: None | collection | function

    :param error_tasks: A set of error tasks.
    :type error_tasks: None | collection | function

    """
    fault = None
    try:
        for task in _get_tasks(tasks):
            task()
        _write(handler)
    except Exception as fault:
        for task in _get_tasks(error_tasks):
            task(fault)
        _write_error(handler, fault)
    finally:
        _log(handler, fault)

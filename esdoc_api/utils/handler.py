# -*- coding: utf-8 -*-
"""
.. module:: utils.handler.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Web request handler utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import inspect

from esdoc_api.utils import (
    config,
    convert,
    runtime as rt
    )



# HTTP header - Content-Type.
_HTTP_HEADER_CONTENT_TYPE = "Content-Type"

# HTTP CORS header.
HTTP_HEADER_Access_Control_Allow_Origin = "Access-Control-Allow-Origin"




class API_Exception(Exception):
    """API exception class.

    """

    def __init__(self, msg):
        """Contructor.

        :param msg: Exception message.
        :type msg: str

        """
        self.message = msg() if inspect.isfunction(msg) else str(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return "ES-DOC API EXCEPTION : {0}".format(repr(self.message))


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
    # Set response content.
    try:
        content = handler.output
    except AttributeError:
        content = None

    # Format html/xml.
    if content and encoding in ('html', 'xml'):
        content = content.strip() if content else str()

    # Format json.
    if encoding == 'json':
        content = content if content else {}
        if 'status' not in content:
            content['status'] = 0

    # Format json-p.
    if content and encoding == 'json':
        try:
            if handler.on_jsonp_load:
                content = "{0}({1});".format(handler.on_jsonp_load, content)
        except AttributeError:
            pass

    # Write.
    handler.write(content)


def _write(handler):
    """Writes a response."""
    # Set response content type.
    try:
        encoding = handler.output_encoding
    except AttributeError:
        encoding = None

    # Set HTTP response Content-Type header.
    if encoding:
        encoding = encoding.lower()
        handler.set_header('Content-Type', _get_mime_type(encoding))

    # Set HTTP response content.
    if encoding:
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
    """Returns a set of tasks for execution.

    """
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
        raise API_Exception(fault)
    finally:
        _log(handler, fault)


def validate_http_content_type(handler, expected_types):
    """Validates HTTP Content-Type request header."""
    if _HTTP_HEADER_CONTENT_TYPE not in handler.request.headers:
        raise ValueError("Content-Type HTTP header is required")
    header = handler.request.headers[_HTTP_HEADER_CONTENT_TYPE]
    if not header in expected_types:
        raise ValueError("Content-Type is unsupported")

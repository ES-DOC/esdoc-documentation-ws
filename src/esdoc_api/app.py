"""
.. module:: app.py
   :copyright: Copyright "Jun 12, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: API entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: utf-8 -*-
import json
import wsgiref.simple_server as wsgi

import tornado.web
import tornado.wsgi

import pyesdoc

import handlers
from utils import config, convert
from utils.runtime import log_api as log



# Ensure that tornado will encode json correctly (i.e. handle dates/UUID's)..
json._default_encoder = convert.JSONEncoder()

# Set of valid container types.
_CONTAINER_TYPE_IOLOOP = 'ioloop'
_CONTAINER_TYPE_WSGI = 'wsgi'
_CONTAINER_TYPES = set([_CONTAINER_TYPE_IOLOOP, _CONTAINER_TYPE_WSGI])

# Default application instance container type.
_DEFAULT_CONTAINER_TYPE = _CONTAINER_TYPE_IOLOOP


def _get_endpoints():
    """Returns map of application endpoints to handlers."""
    endpoints = (
        (r'/2/document/create', handlers.publishing.DocumentCreateRequestHandler),
        (r'/2/document/delete', handlers.publishing.DocumentDeleteRequestHandler),
        (r'/2/document/retrieve', handlers.publishing.DocumentRetrieveRequestHandler),
        (r'/2/document/update', handlers.publishing.DocumentUpdateRequestHandler),
        (r'/2/document/search', handlers.search.DocumentSearchRequestHandler),
        (r'/2/summary/search', handlers.search.SummarySearchRequestHandler),
        (r'/2/summary/search/setup', handlers.search.SummarySearchSetupRequestHandler),
        (r'/2/ops/heartbeat', handlers.ops.HeartbeatRequestHandler),
    )

    log("Endpoint to handler mappings:")
    for url, handler in endpoints:
        log("{0} ---> {1}".format(url, handler))

    return endpoints


def _get_settings():
    """Returns application settings."""
    return {
        "cookie_secret": config.cookie_secret
    }


def _get_app():
    """Returns application instance."""
    return tornado.web.Application(_get_endpoints(),
                                   debug=(config.port==5000),
                                   **_get_settings())


def _run_in_ioloop(app):
    """Runs application instance in an ioloop."""
    app.listen(config.port)
    log("Ready")
    tornado.ioloop.IOLoop.instance().start()


def _run_in_wsgi(app):
    """Runs application instance in a wsgi container."""
    wsgi_app = tornado.wsgi.WSGIAdapter(app)
    wsgi_server = wsgi.make_server('', config.port, wsgi_app)
    log("Ready")
    wsgi_server.serve_forever()


# Map of container types to containers.
_CONTAINERS = {
    _CONTAINER_TYPE_IOLOOP: _run_in_ioloop,
    _CONTAINER_TYPE_WSGI: _run_in_wsgi
}


def run(container_type=_DEFAULT_CONTAINER_TYPE):
    """Runs web service.

    :param str container_type: Type of container within which to run the application instance.

    """
    # Validate inputs.
    if container_type not in _CONTAINER_TYPES:
        msg = "Invalid API application container type.  Valid types are: {0}."
        msg = msg.format(", ".join(_CONTAINER_TYPES))
        raise ValueError(msg)

    log("Initializing")

    # Run application instance in container.
    container = _CONTAINERS[container_type]
    container(_get_app())

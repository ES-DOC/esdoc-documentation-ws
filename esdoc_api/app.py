# -*- coding: utf-8 -*-
"""
.. module:: app.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: API entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import json

import tornado.web

import pyesdoc

from esdoc_api import handlers
from esdoc_api.utils import config
from esdoc_api.utils import convert
from esdoc_api.utils.runtime import log_api as log



# Ensure that tornado will encode json correctly (i.e. handle dates/UUID's).
json._default_encoder = convert.JSONEncoder()


def _get_endpoints():
    """Returns map of application endpoints to handlers.

    """
    endpoints = {
        (r'/2/document/create', handlers.publishing.DocumentCreateRequestHandler),
        (r'/2/document/delete', handlers.publishing.DocumentDeleteRequestHandler),
        (r'/2/document/retrieve', handlers.publishing.DocumentRetrieveRequestHandler),
        (r'/2/document/search', handlers.search.DocumentSearchRequestHandler),
        (r'/2/summary/search', handlers.search.SummarySearchRequestHandler),
        (r'/2/summary/search/setup', handlers.search.SummarySearchSetupRequestHandler),
        (r'/heartbeat', handlers.ops.HeartbeatRequestHandler),
    }

    log("Endpoint to handler mappings:")
    for url, handler in endpoints:
        log("{0} ---> {1}".format(url, handler))

    return endpoints


def _get_settings():
    """Returns application settings.

    """
    return {
        "cookie_secret": config.cookie_secret
    }


def _get_app():
    """Returns application instance.

    """
    return tornado.web.Application(_get_endpoints(),
                                   debug=(config.mode == 'dev'),
                                   **_get_settings())


def run():
    """Runs web service.

    """
    log("Initializing")

    # Initialise archive usage.
    pyesdoc.archive.init()

    # Run web-service.
    app = _get_app()
    app.listen(config.port)
    log("Ready")
    tornado.ioloop.IOLoop.instance().start()


def stop():
    """Stops web service.

    """
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(lambda x: x.stop(), ioloop)

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
from esdoc_api import schemas
from esdoc_api.utils import config
from esdoc_api.utils import convertor
from esdoc_api.utils.logger import log_web as log



# Ensure that tornado will encode json correctly (i.e. handle dates/UUID's).
json._default_encoder = convertor.JSONEncoder()


def _get_app_endpoints():
    """Returns map of application endpoints to handlers.

    """
    result = {
        (r'/', handlers.ops.HeartbeatRequestHandler),
        # (r'/2/document/create', handlers.publishing.DocumentCreateRequestHandler),
        # (r'/2/document/delete', handlers.publishing.DocumentDeleteRequestHandler),
        (r'/2/document/retrieve', handlers.publishing.DocumentRetrieveRequestHandler),
        # (r'/2/document/update', handlers.publishing.DocumentUpdateRequestHandler),
        (r'/2/document/search-drs', handlers.search.DocumentByDRSSearchRequestHandler),
        (r'/2/document/search-externalid', handlers.search.DocumentByExternalIDSearchRequestHandler),
        (r'/2/document/search-id', handlers.search.DocumentByIDSearchRequestHandler),
        (r'/2/document/search-name', handlers.search.DocumentByNameSearchRequestHandler),
        (r'/2/summary/search', handlers.search.SummarySearchRequestHandler),
        (r'/2/summary/search/setup', handlers.search.SummarySearchSetupRequestHandler)
    }

    return result


def _get_app_settings():
    """Returns application settings.

    """
    return {
        "cookie_secret": config.cookie_secret
    }


def _get_app():
    """Returns application instance.

    """
    # Initialise archive usage.
    pyesdoc.archive.init()

    # Get endpoints.
    endpoints = _get_app_endpoints()
    log("Endpoint to handler mappings:")
    for url, handler in sorted(endpoints, key=lambda i: i[0]):
        log("{0} ---> {1}".format(url, str(handler).split(".")[-1][0:-2]))

    # Initialise JSON schemas.
    schemas.init([i[0] for i in endpoints])

    # Convert endpoints to tornado URLSpec instances.
    endpoints = [tornado.web.url(i[0], i[1]) for i in endpoints]

    # Return app instance.
    return tornado.web.Application(endpoints,
                                   debug=(config.mode == 'dev'),
                                   **_get_app_settings())


def run():
    """Runs web service.

    """
    log("Initializing")

    # Run web-service.
    app = _get_app()
    app.listen(config.port)
    log("Running @ port {}".format(config.port))
    tornado.ioloop.IOLoop.instance().start()


def stop():
    """Stops web service.

    """
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(lambda x: x.stop(), ioloop)

"""
.. module:: app.py
   :copyright: Copyright "Jun 12, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Web-service entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: utf-8 -*-

# Module imports.
import os

import tornado
from tornado.web import Application
import pyesdoc

from . import handlers, utils



def _get_path_to_front_end():
    """Return path to the front end javascript application."""
    # N.B. deriving path on assumption that software
    # has been installed using the prodiguer bootstrapper.

    # Get directory to ES-DOC repos.
    repos = os.path.dirname(__file__)
    for i in range(4):
        repos = os.path.dirname(repos)

    # Get directory to front end source code.
    path = os.path.join(repos, 'esdoc-fe')
    path = os.path.join(path, 'src')
    utils.rt.log_api("Front-end @ {0}".format(path))

    return path


def _get_app_routes():
    """Returns supported app routes."""
    return (
        (r'/1/document/create', handlers.publishing.DocumentCreateRequestHandler),
        (r'/1/document/delete', handlers.publishing.DocumentDeleteRequestHandler),
        (r'/1/document/retrieve', handlers.publishing.DocumentRetrieveRequestHandler),
        (r'/1/document/update', handlers.publishing.DocumentUpdateRequestHandler),
        (r'/1/document/search', handlers.search.DocumentSearchRequestHandler),
        (r'/1/summary/search', handlers.search.SummarySearchRequestHandler),
        (r'/1/summary/search/setup', handlers.search.SummarySearchSetupRequestHandler),
        (r'/1/ops/heartbeat', handlers.ops.HeartbeatRequestHandler),
    )


def _get_app_settings():
    """Returns app settings."""
    return {
        "cookie_secret": utils.config.api.cookie_secret,
        # "static_path": _get_path_to_front_end()
    }


def run():
    """Runs the web service process."""
    utils.rt.log_api("Initializing")

    # Build routes.
    routes = _get_app_routes()
    utils.rt.log_api("URL to handler mapping:")
    for url, handler in routes:
        utils.rt.log_api("{0} ---> {1}".format(url, handler))

    # Instantiate.
    app = Application(routes,
                      debug=not utils.config.core.mode=='prod',
                      **_get_app_settings())

    # Listen.
    app.listen(utils.config.api.port)
    utils.rt.log_api("Ready")

    # Start io loop.
    tornado.ioloop.IOLoop.instance().start()

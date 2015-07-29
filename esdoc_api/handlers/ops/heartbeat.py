# -*- coding: utf-8 -*-

"""
.. module:: handlers.ops.heartbeat.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Operations heartbeat request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import datetime

import tornado

from esdoc_api import utils



class HeartbeatRequestHandler(tornado.web.RequestHandler):
    """Operations heartbeat request handler.

    """
    def get(self):
        """HTTP GET handler.

        """
        self.output_encoding = 'json'
        self.output = {
            "message": "ES-DOC web service API is operational @ {}".format(datetime.datetime.now())
        }
        utils.h.invoke(self)

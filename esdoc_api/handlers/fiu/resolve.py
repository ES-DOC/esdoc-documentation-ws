# -*- coding: utf-8 -*-

"""
.. module:: handlers.resolve.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Resolve further info URL endpoint.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime as dt

import tornado

import esdoc_api
from esdoc_api.utils.http import process_request



class ResolveRequestHandler(tornado.web.RequestHandler):
    """Resolve further info URL handler.

    """
    def get(self, mip_era):
        """HTTP GET handler.

        """
        def _set_output():
            """Sets response to be returned to client.

            """

            self.output = {
                "message": "ES-DOC further info URL service is operational @ {}".format(dt.datetime.now()),
                "version": esdoc_api.__version__,
                "mip_era": mip_era
                # "further_info": further_info
            }

            print self.output


        print mip_era

        # Process request.
        process_request(self, _set_output)

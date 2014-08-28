# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.retrieve.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing retrieve document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado




class DocumentRetrieveRequestHandler(tornado.web.RequestHandler):
    """Publishing retrieve document request handler.

    """
    def get(self):
        """HTTP GET handler."""
        print "TODO retrieve instance"


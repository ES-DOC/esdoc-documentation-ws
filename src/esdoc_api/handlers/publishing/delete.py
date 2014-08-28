# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.delete.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing delete document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado




class DocumentDeleteRequestHandler(tornado.web.RequestHandler):
    """Publishing delete document request handler.

    """
    def post(self):
        """HTTP POST handler."""
        print "TODO delete instance"


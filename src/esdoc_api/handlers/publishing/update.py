# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.update.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing update document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado




class DocumentUpdateRequestHandler(tornado.web.RequestHandler):
    """Publishing update document request handler.

    """
    def post(self):
        """HTTP POST handler."""
        print "TODO update instance"


# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.create.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing create document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado




class DocumentCreateRequestHandler(tornado.web.RequestHandler):
    """Publishing create document request handler.

    """
    def post(self):
        """HTTP POST handler."""
        print "TODO create instance"


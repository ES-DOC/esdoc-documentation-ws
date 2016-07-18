# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.__init__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing package initializer.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.handlers.publishing.create import DocumentCreateRequestHandler
from esdoc_api.handlers.publishing.delete import DocumentDeleteRequestHandler
from esdoc_api.handlers.publishing.retrieve import DocumentRetrieveRequestHandler
from esdoc_api.handlers.publishing.update import DocumentUpdateRequestHandler

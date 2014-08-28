# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.__init__.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing package initializer.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from .create import DocumentCreateRequestHandler
from .delete import DocumentDeleteRequestHandler
from .retrieve import DocumentRetrieveRequestHandler
from .update import DocumentUpdateRequestHandler

# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.__init__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search package initializer.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.handlers.search.document_by_drs import DocumentByDRSSearchRequestHandler
from esdoc_api.handlers.search.document_by_external_id import DocumentByExternalIDSearchRequestHandler
from esdoc_api.handlers.search.document_by_id import DocumentByIDSearchRequestHandler
from esdoc_api.handlers.search.document_by_name import DocumentByNameSearchRequestHandler
from esdoc_api.handlers.search.summary import SummarySearchRequestHandler
from esdoc_api.handlers.search.summary_setup import SummarySearchSetupRequestHandler

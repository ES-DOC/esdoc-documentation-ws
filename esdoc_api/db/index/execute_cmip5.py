"""
.. module:: esdoc_api.db.index.execute_cmip5.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Indexes archived CMIP5 documents.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
# -*- coding: utf-8 -*-
from esdoc_api.db import (
    cache,
    dao,
    models,
    utils
    )
from esdoc_api.db.index.cim_v1.model_component.indexer import index as index_model
from esdoc_api.db.index.cim_v1.numerical_experiment.indexer import index as index_experiment
from esdoc_api.utils import runtime as rt



# Project whose facets are being indexed.
_PROJECT = "CMIP5"

# Encoding used to load documents.
_ENCODING = "json"

# Ontology used to load documents.
_ONTOLOGY = "cim.1"

# Ontology used to load documents.
_LANGUAGE = "en"

# CIM type helper vars.
_CIM_V1_EXPERIMENT = "cim.1.activity.numericalexperiment"
_CIM_V1_MODEL = "cim.1.software.modelcomponent"


class _ProcessingContextInfo(object):
    """Encapsulates processing context information."""
    def __init__(self):
        self.encoding = _ENCODING
        self.experiments = []
        self.models = []
        self.ontology = _ONTOLOGY
        self.project = _PROJECT.lower()


def _load_docs(ctx):
    """Loads documents to be indexed."""

    def get_docs(doc_type):
        """Gets documents filtered by document type.

        """
        return dao.get_document_by_type(ctx.project.id, doc_type, False)


    def decode(docs):
        """Gets decoded document collection.

        """
        docs = map(lambda doc: utils.get_archived_document(doc), docs)

        return sorted(docs, key=lambda doc: doc.short_name.upper())


    def get_collection(doc_type, key_formatter):
        """Gets document collection for processing.

        """
        collection = {}
        for doc in get_docs(doc_type):
            key = key_formatter(doc)
            if key not in collection or \
               doc.version > collection[key].version:
                collection[key] = doc

        return decode(collection.values())


    def get_key(doc):
        """Returns document key.

        """
        institute = cache.get_name(models.Institute, doc.institute)
        name = doc.name.upper()

        return "{0}--{1}".format(institute, name)


    ctx.experiments = get_collection(_CIM_V1_EXPERIMENT, get_key)
    ctx.models = get_collection(_CIM_V1_MODEL, get_key)


def _index(ctx):
    """Indexes loaded documents."""
    def build(collection, indexer):
        """Builds index."""
        for doc in collection:
            indexer(ctx.project.id, doc)

    build(ctx.experiments, index_experiment)
    build(ctx.models, index_model)


def execute():
    """Executes facet indexing from cmip5 project."""
    ctx = _ProcessingContextInfo()
    for func, msg in (
        (_load_docs, "loading documents"),
        (_index, "building indexes"),
        ):
        rt.log("INDEXING :: {0} :: {1}".format(_PROJECT, msg))
        func(ctx)
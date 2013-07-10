"""
.. module:: esdoc_api.lib.repo.models.__init__.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of models supported by ES-DOC API.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.repo.models.utils import (
    Entity,
    ESDOCEntity as Entity,
    EntityConvertor,
    EntityConvertor as Convertor,
    metadata
    )
from esdoc_api.lib.repo.models.docs import *
from esdoc_api.lib.repo.models.facets import *
from esdoc_api.lib.repo.models.ingest import *
from esdoc_api.lib.repo.models.vocab import *


# Set of supported model types - useful for testing scenarios.
supported_types = [
    # ... docs
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentRepresentation,
    DocumentSubDocument,
    DocumentSummary,
    # ... facets
    Facet,
    FacetRelation,
    FacetRelationType,
    FacetType,
    # ... ingest
    IngestEndpoint,
    IngestHistory,
    IngestURL,
    # ... vocab
    DocumentEncoding,
    DocumentLanguage,
    DocumentOntology,
    DocumentType,
    IngestState,
    Institute,
    Project
]

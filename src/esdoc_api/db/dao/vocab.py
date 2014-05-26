"""
.. module:: vocab.py
   :platform: Unix
   :synopsis: Data access operations across vocab domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import sqlalchemy as sa

from . core import (
    get_by_facet,
    )
from .. models import (
    Document,
    DocumentLanguage,
    DocumentOntology,
    IngestEndpoint,
    IngestURL,
)
import esdoc_api.pyesdoc as pyesdoc
from .. import session



# Module exports.
__all__ = [
    'get_doc_language',
    'get_doc_ontology',
    'get_ingest_endpoints',
    'get_ingest_endpoint',
    'get_ingest_url',
    'get_project_institute_counts'
]



def get_doc_ontology(name, version=None):
    """Returns a DocumentOntology instance with matching name & version.

    :param name: Ontology name.
    :type name: str

    :param version: Ontology version.
    :type version: str

    :returns: First DocumentOntology instance with matching name & version.
    :rtype: esdoc_api.db.models.DocumentOntology

    """
    if version is not None:
        name += '.'
        name += str(version)

    qry = session.query(DocumentOntology)

    qry = qry.filter(DocumentOntology.Name==name.lower())

    return qry.first()


def get_doc_language(code=pyesdoc.ESDOC_DEFAULT_LANGUAGE):
    """Returns a DocumentLanguage instance by it's code.

    :param type: A supported entity type.
    :type type: class

    :param name: Entity code.
    :type name: str

    :returns: First DocumentLanguage with matching code.
    :rtype: esdoc_api.db.models.DocumentLanguage

    """
    return get_by_facet(DocumentLanguage,
                        DocumentLanguage.Code==code.lower())


def get_ingest_endpoint(url):
    """Returns an IngestEndpoint instance by it's url.

    :param url: URL of an IngestEndpoint instance to be retrieved.
    :type url: str

    :returns: First IngestEndpoint instance with matching url.
    :rtype: esdoc_api.db.models.IngestEndpoint

    """
    return get_by_facet(IngestEndpoint,
                        IngestEndpoint.IngestURL==url)


def get_ingest_endpoints():
    """Returns a list of active IngestEndpoint instances.

    :returns: List of active IngestEndpoint instances.
    :rtype: list

    """
    qry = session.query(IngestEndpoint)

    qry = qry.filter(IngestEndpoint.IsActive==True)
    qry = qry.order_by(IngestEndpoint.Priority.desc())

    return qry.all()


def get_ingest_url(url):
    """Returns an IngestURL instance by it's url.

    :param url: URL of an IngestURL instance to be retrieved.
    :type url: str

    :returns: First IngestURL instance with matching url.
    :rtype: esdoc_api.db.models.IngestURL

    """
    return get_by_facet(IngestURL, IngestURL.URL==url)


def get_project_institute_counts():
    """Returns institute counts grouped by project.

    :returns: List of counts over a project's institutes.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.Institute_ID),
                      Document.Project_ID,
                      Document.Institute_ID)

    qry = qry.group_by(Document.Project_ID)
    qry = qry.group_by(Document.Institute_ID)

    return qry.all()

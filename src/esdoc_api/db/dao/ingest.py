"""
.. module:: ingest.py
   :platform: Unix
   :synopsis: Data access operations across ingest domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from . core import (
    get_by_facet,
    )
from .. models import (
    IngestEndpoint,
    IngestURL,
)
from .. import session



# Module exports.
__all__ = [
    'get_ingest_endpoints',
    'get_ingest_endpoint',
    'get_ingest_url',
]



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

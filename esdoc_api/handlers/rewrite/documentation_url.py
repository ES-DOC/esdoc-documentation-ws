# -*- coding: utf-8 -*-

"""
.. module:: handlers.rewrite.documentation_url.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Rewrites documentation URL's.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api.utils.http import log_error
from esdoc_api.utils.http import write_error



# Map of project to cim document types.
DOC_TYPES = {
    "cmip5": {
        "experiments": "cim.1.activity.NumericalExperiment",
        "models": "cim.1.software.ModelComponent",
        "platforms": "cim.1.shared.Platform",
        "simulations": "cim.1.misc.DocumentSet",
    },
    "cmip6": {
        "experiments": "cim.2.designing.NumericalExperiment",
        "mips": "cim.2.designing.Project",
        "models": "cim.2.science.Model",
    },
    "dcmip-2012": {
        "models": "cim.1.software.ModelComponent",
    },
    "esps": {
        "models": "cim.1.software.ModelComponent",
    },
}

# Map of project to supported cim document types.
DEFAULT_DOC_TYPES = {
    "cmip5": "experiments",
    "cmip6": "mips",
    "dcmip-2012": "models",
    "esps": "models"
}

# Implicit support for draft project documents.
for key, value in DOC_TYPES.items():
    DOC_TYPES["{}-draft".format(key)] = value
for key, value in DEFAULT_DOC_TYPES.items():
    DEFAULT_DOC_TYPES["{}-draft".format(key)] = value

# Map of target URL's.
_URLS = {
    "search": {
        "prod": "http://search.es-doc.org",
        "test": "http://test.search.es-doc.org",
        "dev": "http://search.es-doc.org",
    },
    "view": {
        "prod": "http://view.es-doc.org",
        "test": "http://test.view.es-doc.org",
        "dev": "http://view.es-doc.org",
    }
}

# Map of target URL's params.
_URL_PARAMS = {
    "search": "/?project={0}&documentType={1}&client={2}",
    "view": "/?renderMethod=name&project={0}&type={1}&client={2}&name={3}"
}

# Query parameter names.
_PARAM_CLIENT_ID = 'client'


class DocumentationURLRewriteRequestHandler(tornado.web.RequestHandler):
    """Rewrites viewer URL requests.

    """
    def get(self, project, doc_type=None, doc_name=None):
        """HTTP GET handler.

        """
        project, doc_type, doc_name = \
            _reformat_inputs(project, doc_type, doc_name)
        if _validate_request(self, project, doc_type):
            url = _get_redirect_url(self, project, doc_type, doc_name)
            self.redirect(url, permanent=False)


def _reformat_inputs(project, doc_type, doc_name):
    """Reforms request parameters.

    """
    project = unicode(project).strip().lower()
    if len(project) == 0:
        project = None
    if doc_type is not None:
        doc_type = unicode(doc_type).strip().lower()
        if len(doc_type) == 0:
            doc_type = None
    elif project in DEFAULT_DOC_TYPES:
        doc_type = DEFAULT_DOC_TYPES[project]
    if doc_name is not None:
        doc_name = unicode(doc_name).strip().lower()
        if len(doc_name) == 0:
            doc_name = None

    # Reroute cmip6 to cmip6-draft.
    if project == u"cmip6":
        project = "cmip6-draft"

    return project, doc_type, doc_name


def _validate_request(handler, project, doc_type):
    """Validates request parameters.

    """
    err = None
    if project not in DOC_TYPES:
        err = ValueError("Unsupported project")
    elif doc_type not in DOC_TYPES[project]:
        err = ValueError("Unsupported project document type")
    if err is not None:
        log_error(handler, err)
        write_error(handler, err)

    return err is None


def _get_redirect_url(handler, project, doc_type, doc_name):
    """Gets redirect url.

    """
    # Set URL type.
    url_type = "search" if doc_name is None else "view"

    # Set URL host type.
    if 'localhost' in handler.request.host:
        url_host_type = "dev"
    elif 'test' in handler.request.host:
        url_host_type = "test"
    else:
        url_host_type = "prod"

    # Set URL params.
    url_params = _URL_PARAMS[url_type].format(
        project,
        DOC_TYPES[project][doc_type],
        handler.get_query_argument(_PARAM_CLIENT_ID, "esdoc-url-rewrite"),
        doc_name
        )

    return "{}{}".format(_URLS[url_type][url_host_type], url_params)

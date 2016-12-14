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
        # Reformat inputs.
        project = unicode(project).strip().lower()
        if len(project) == 0:
            project = None
        if doc_type is not None:
            doc_type = unicode(doc_type).strip().lower()
            if len(doc_type) == 0:
                doc_type = None
        if doc_name is not None:
            doc_name = unicode(doc_name).strip().lower()
            if len(doc_name) == 0:
                doc_name = None
        client = self.get_query_argument(_PARAM_CLIENT_ID, "esdoc-url-rewrite")

        # Set defaults.
        if doc_type is None and project in DEFAULT_DOC_TYPES:
            doc_type = DEFAULT_DOC_TYPES[project]

        # Validate inputs.
        err = None
        if project not in DOC_TYPES:
            err = ValueError("Unsupported project")
        elif doc_type not in DOC_TYPES[project]:
            err = ValueError("Unsupported project document type")
        if err is not None:
            log_error(self, err)
            write_error(self, err)
            return

        # Set URL type.
        url_type = "search" if doc_name is None else "view"

        # Set URL host type.
        if 'localhost' in self.request.host:
            url_host_type = "dev"
        elif 'test' in self.request.host:
            url_host_type = "test"
        else:
            url_host_type = "prod"

        # Set URL params.
        url_params = _URL_PARAMS[url_type].format(
            project,
            DOC_TYPES[project][doc_type],
            client,
            doc_name
            )

        # Set URL.
        url = "{}{}".format(_URLS[url_type][url_host_type], url_params)

        # Redirect user.
        self.redirect(url, permanent=False)

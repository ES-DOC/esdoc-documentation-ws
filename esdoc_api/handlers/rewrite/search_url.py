# -*- coding: utf-8 -*-

"""
.. module:: handlers.heartbeat.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC - heartbeat endpoint.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api.utils.http import log_error
from esdoc_api.utils.http import write_error



# Map of project to cim document types.
PROJECT_DOC_TYPES = {
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

# Implicit support for draft project documents.
for key, value in PROJECT_DOC_TYPES.items():
    PROJECT_DOC_TYPES["{}-draft".format(key)] = value

# Map of execution modes to viewer URL.
_SEARCH_URL = {
    "prod": "http://search.es-doc.org",
    "test": "http://test.search.es-doc.org",
    "dev": "http://search.es-doc.org",
}

# Viewer URL query parameters.
_URL_QUERY_PARAMS = "/?project={}&documentType={}&client={}"

# Query parameter names.
_PARAM_CLIENT_ID = 'client'


class SearchURLRewriteRequestHandler(tornado.web.RequestHandler):
    """Rewrites search URL requests.

    """
    def get(self, project, doc_type):
        """HTTP GET handler.

        """
        # Reformat inputs.
        project = unicode(project).strip().lower()
        doc_type = unicode(doc_type).strip().lower()
        client = self.get_query_argument(_PARAM_CLIENT_ID, "esdoc-url-rewrite")

        # Escape if invalid.
        if project not in PROJECT_DOC_TYPES or doc_type not in PROJECT_DOC_TYPES[project]:
            err = ValueError("Unsupported project / document-type")
            log_error(self, err)
            write_error(self, err)
            return

        # Set viewer URL params.
        url_params = _URL_QUERY_PARAMS.format(
            project,
            PROJECT_DOC_TYPES[project][doc_type],
            client
            )

        # Set mode.
        if 'localhost' in self.request.host:
            mode = "dev"
        elif 'test' in self.request.host:
            mode = "test"
        else:
            mode = "prod"

        # Redirect user.
        url = "{}{}".format(_SEARCH_URL[mode], url_params)
        self.redirect(url, permanent=False)

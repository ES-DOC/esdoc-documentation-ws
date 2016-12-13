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
        "experiments": "cim.1.activity.numericalexperiment",
        "models": "cim.1.software.modelcomponent",
        "platforms": "cim.1.shared.platform",
        "simulations": "cim.1.misc.documentset",
    },
    "cmip6": {
        "experiments": "cim.2.designing.numericalexperiment",
        "mips": "cim.2.designing.project",
        "models": "cim.2.science.model",
    },
    "dcmip-2012": {
        "models": "cim.1.software.modelcomponent",
    },
    "esps": {
        "models": "cim.1.software.modelcomponent",
    },
}

# Implicit support for draft project documents.
for key, value in PROJECT_DOC_TYPES.items():
    PROJECT_DOC_TYPES["{}-draft".format(key)] = value

# Map of execution modes to viewer URL.
_VIEWER_URL = {
    "prod": "http://view.es-doc.org",
    "test": "http://test.view.es-doc.org",
    "dev": "http://view.es-doc.org",
}

# Viewer URL query parameters.
_URL_QUERY_PARAMS = "/?renderMethod=name&project={}&name={}&type={}&client={}"

# Query parameter names.
_PARAM_CLIENT_ID = 'client'


class ViewerURLRewriteRequestHandler(tornado.web.RequestHandler):
    """Rewrites viewer URL requests.

    """
    def get(self, project, doc_type, doc_name):
        """HTTP GET handler.

        """
        # Reformat inputs.
        doc_name = unicode(doc_name).strip().lower()
        doc_type = unicode(doc_type).strip().lower()
        project = unicode(project).strip().lower()
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
            doc_name,
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
        url = "{}{}".format(_VIEWER_URL[mode], url_params)
        self.redirect(url, permanent=False)

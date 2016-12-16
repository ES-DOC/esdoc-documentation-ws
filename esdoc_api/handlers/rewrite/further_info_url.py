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



# Set of supported projects.
PROJECT = {
    "cmip6",
}

# Query parameter names.
_PARAM_CLIENT_ID = 'client'


class FurtherInfoURLRewriteRequestHandler(tornado.web.RequestHandler):
    """Rewrites viewer URL requests.

    """
    def get(self, mip_era, further_info):
        """HTTP GET handler.

        """
        # Reformat & unpack.
        mip_era, further_info = _reformat_inputs(mip_era, further_info)
        institution_id, source_id, experiment_id, variant_label = further_info.split('.')

        print mip_era, institution_id, source_id, experiment_id, variant_label


def _reformat_inputs(mip_era, further_info):
    """Reforms request parameters.

    """
    mip_era = unicode(mip_era).strip().lower()
    if len(mip_era) == 0:
        mip_era = None

    further_info = unicode(further_info).strip().lower()
    if len(further_info) == 0:
        further_info = None

    # Reroute cmip6 to cmip6-draft.
    if mip_era == u"cmip6":
        mip_era = "cmip6-draft"

    return mip_era, further_info

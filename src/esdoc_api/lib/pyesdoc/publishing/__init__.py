from .. import utils
from .. import serialization

import requests



# API url option name.
_OPT_API_URL = 'api_url'

# Publishign API endpoint.
_EP_PUBLISHING = 'publishing'


HTTP_RESPONSE_STATUS_200 = 200


def _get_api_url(ep):
    """Helper function to return api endpoint url."""
    return utils.get_option(_OPT_API_URL) + '/1/{0}'.format(ep)


def retrieve(uid, version):
    url = _get_api_url(_EP_PUBLISHING)
    url += '/{0}/{1}'.format(uid, version)

    r = requests.get(url)

    if r.status_code == HTTP_RESPONSE_STATUS_200:
        print serialization.decode(r.text, serialization.ESDOC_ENCODING_JSON)

    
    # call out to external API.

    # upon success:
        # decode json to doc.
        # return doc

    # upon failure:
        # return None

    # upon error
        # raise exception



import pyesdoc

from esdoc_api.lib.controllers.base_controller import BaseController
from pylons import request
import esdoc_api.lib.utils.http_utils as http_utils



class BaseAPIController(BaseController):
    """Base class for all ES-DOC API controllers.

    """
    @property
    def controller_type_description(self):
        """Gets type controller type description.

        """
        return "WEB SERVICE"


    def get_response_content_type(self):
        """Returns http reponse content type derived from request content type http header.

        """
        if request.params.has_key('encoding'):
            encoding = request.params['encoding'].lower()
            if encoding in pyesdoc.ESDOC_ENCODING_HTTP_MEDIA_TYPES:
                return pyesdoc.ESDOC_ENCODING_HTTP_MEDIA_TYPES[encoding]

        return http_utils.HTTP_MEDIA_TYPE_JSON

"""Controller decorator functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from decorator import decorator
import logging
import sys
import httplib
import simplejson
import warnings
import datetime
from pylons import request
from pylons import response
from pylons import session
from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons.controllers.util import redirect
from pylons.decorators.util import get_pylons
from pylons.decorators import jsonify
from symbol import except_clause
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.mimehelper import MIMETypes
from webhelpers.mimehelper import mimetypes
from webhelpers.pylonslib.secure_form import secure_form

__all__ = ['jsonify', '_jsonify']

log = logging.getLogger(__name__)


class JSONEncoder(simplejson.JSONEncoder):
    """
    Extends simplejson to handle specific types.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace('T', ' ')
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        else:
            return simplejson.JSONEncoder.default(self, obj)


def _jsonify(cb=None):
    """Action decorator that formats output for JSON

    Given a function that will return content, this decorator will turn
    the result into JSON, with a content-type of 'application/json' and
    output it.

    ``cb``
        If set, and if the request includes a param whose key equals to
        the value of this argument, then the JSON output is wrapped in
        a JavaScript call and the Content-Type header is set to
        'text/javascript'. For example, if ``cb`` is set to ``cb``, and
        if the request includes ``cb=process`` then the output will
        look like ``process({"some": "json"});``.
    ``**dumps_kwargs``
        Arguments to pass to the ``simplejson.dumps`` function. Can be
        useful to specify a specific encoder (using the ``cls``
        argument).
    Use the ``jsonify`` decorator if what you need is JSON and if you
    don't need to pass specific arguments to ``simplejson.dumps``.
    (``jsonify`` is defined as ``_jsonify()``.)
    """

    def wrapper(func, *args, **kwargs):
        pylons = get_pylons(args)

        # Format json data.
        data = func(*args, **kwargs)
        output = JSONEncoder().encode(data)

        # Response content type = either jsonp or json.
        cb_name = pylons.request.params.get(cb)
        if cb_name is not None:
            pylons.response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
        else:
            pylons.response.headers['Content-Type'] = 'application/json'


        # JSONP - wrap response in callback fn pointer.
        if cb_name is not None:
            output = str(cb_name) + '(' + output + ');'
            log.debug("Returning JSONP wrapped action output")

        else:
            if isinstance(data, (list, tuple)):
                msg = "JSON responses with Array envelopes are susceptible to " \
                      "cross-site data leak attacks, see " \
                      "http://pylonshq.com/warnings/JSONArray"
                warnings.warn(msg, Warning, 2)
                log.warning(msg)
            log.debug("Returning JSON wrapped action output")

        return output

    return decorator(wrapper)
jsonify = _jsonify('onJSONPLoad')



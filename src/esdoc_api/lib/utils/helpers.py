"""
Helper functions

Functions typically used by templates, but also by Controllers. Available to templates as 'h'.
"""
# Python standard packages.
from decorator import decorator
import logging
import sys
import httplib
import json
import simplejson
import warnings
import time
from datetime import datetime
from symbol import except_clause

# Pylons packages.
from pylons import config
from pylons import request
from pylons import response
from pylons import session
from pylons import tmpl_context as c
from pylons import url
from pylons.controllers.util import abort
from pylons.controllers.util import redirect
from pylons.decorators.util import get_pylons

# Web helpers packages.
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.mimehelper import MIMETypes
from webhelpers.mimehelper import mimetypes
from webhelpers.pylonslib.secure_form import secure_form

log = logging.getLogger(__name__)


def create_exception_response(e, status_code=httplib.BAD_REQUEST):
    """Given an exception, return an appropriate response.

    Also, set the response.status_code.  The default status code is
    httplib.BAD_REQUEST simply because that's the most common case.

    """
    response.status_code = status_code
    return dict(exception=e.__class__.__name__, errorMessage=str(e))



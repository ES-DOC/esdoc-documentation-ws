"""The base Controller API

Provides the BaseController class for subclassing.
"""
# Builtin packages.
import abc
import logging
import sys
import httplib
import json
import simplejson
import warnings
import time
from abc import ABCMeta
from abc import abstractproperty
from datetime import datetime
from decorator import decorator
from symbol import except_clause

# Pylons packages.
from pylons import config
from pylons import config as pylons_config
from pylons import request
from pylons import response
from pylons import session
from pylons import tmpl_context as c
from pylons import app_globals
from pylons import app_globals as g
from pylons import url
from pylons.controllers import WSGIController
from pylons.controllers.util import abort
from pylons.controllers.util import redirect
from pylons.decorators.cache import *
from pylons.decorators.util import get_pylons
from pylons.templating import render_mako as render
from beaker.cache import cache_region

# Web helpers packages.
from webhelpers.html import literal
from webhelpers.html.tags import *
from webhelpers.mimehelper import MIMETypes
from webhelpers.mimehelper import mimetypes
from webhelpers.pylonslib.secure_form import secure_form

# LXML package.
import lxml
from lxml import etree as et

# Portal packages.
from esdoc_api.lib.utils.helpers import *
import esdoc_api.lib.utils.helpers as h
from esdoc_api.lib.controllers.cache_data import CacheData
from esdoc_api.models import *
from esdoc_api.models.entities import *
from esdoc_api.models.search import *


class BaseController(WSGIController):
    """
    Base class for all non-Metafor controllers.
    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Initialises controller state.
        """
        # Set common context info.
        c.timestamp = datetime.now()
        c.path = request.path

    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            print "{0} CONTROLLER INVOKE START :: {1} :: {2}".format(self.controller_type_description, environ['pylons.routes_dict']['controller'], environ['pylons.routes_dict']['action'])
            return WSGIController.__call__(self, environ, start_response)
        finally:
            # Ensure ORM session is killed.
            meta.Session.close()
            print "{0} CONTROLLER INVOKE END :: {1} :: {2}".format(self.controller_type_description, environ['pylons.routes_dict']['controller'], environ['pylons.routes_dict']['action'])


    @abstractproperty
    def controller_type_description(self):
        """
        Gets type controller type description.
        """
        pass


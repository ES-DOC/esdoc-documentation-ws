"""The base Controller API

Provides the BaseController class for subclassing.
"""
# Builtin packages.
import abc
import logging
import sys
import httplib
import json
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

# Sqlalchemy packages.
from sqlalchemy import engine_from_config

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
from esdoc_api.db.models import *
from esdoc_api.lib.utils.helpers import *
import esdoc_api.db.session as repo_session
import esdoc_api.lib.utils.helpers as h
import esdoc_api.db.cache as cache
import esdoc_api.lib.utils.runtime as rt



class BaseController(WSGIController):
    """Base class for all ES-DOC API controllers.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta
    

    def __before__(self, action, **kwargs):
        """Pre action invocation handler.

        """
        rt.log("{0} CONTROLLER INVOKE START :: {1} :: {2}".format(
            self.controller_type_description,
            action,
            datetime.now()))

        # Set common context info.
        c.timestamp = datetime.now()
        c.path = request.path

        # Set cache.
        cache.load()
        c.cache = cache


    def __after__(self, action, **kwargs):
        """Post action invocation handler.

        """
        rt.log("{0} CONTROLLER INVOKE END :: {1} :: {2}".format(
            self.controller_type_description,
            action,
            datetime.now()))


    @abstractproperty
    def controller_type_description(self):
        """
        Gets type controller type description.
        """
        pass


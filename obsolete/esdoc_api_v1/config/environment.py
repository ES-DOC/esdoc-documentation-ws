# -*- coding: utf-8 -*-

"""Pylons environment configuration"""
import os
import sys

from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

from esdoc_api.config.routing import make_map
import esdoc_api.lib.utils.app_globals as app_globals
import esdoc_api.lib.utils.helpers
import esdoc_api.lib.utils.runtime as rt

import pyesdoc.db.session as db_session



def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()

    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'static'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='esdoc_api', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = esdoc_api.lib.utils.helpers

    # Setup cache object as early as possible
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)

    # Setup the SQLAlchemy database engine
    db_session.start(engine_from_config(config, 'sqlalchemy.'))

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)

    # Allow developer to see environment.
    rt.log("ENVIRONMENT :: PYLONS :: ROOT :: {0}.".format(str(root)))
    rt.log("ENVIRONMENT :: PYLONS :: TEMPLATES :: {0}.".format(str(paths['templates'])))
    rt.log("ENVIRONMENT :: PYLONS :: CONTROLLERS :: {0}.".format(str(paths['controllers'])))
    rt.log("ENVIRONMENT :: PYLONS :: STATIC FILES :: {0}.".format(str(paths['static_files'])))
    for path in sys.path:
        rt.log("ENVIRONMENT :: PYTHON PATH :: {0}.".format(path))
    for key, value in config.items():
        rt.log("ENVIRONMENT :: CONFIG ITEM :: {0} :: {1}.".format(key, str(value)))

    return config


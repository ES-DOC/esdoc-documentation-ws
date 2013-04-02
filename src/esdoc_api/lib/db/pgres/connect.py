"""Connects to the database so that data-access operations can be executed.

"""
"""Connect to CIM postgres database for use in scripting sessions.

"""

# Module imports.
import logging
import os

from elixir import *

from esdoc_api.models.entities import *
from esdoc_api.models.search import *


def _get_user_name():
    """Returns current user name.
    
    """
    username = None
    try:
        import pwd
        username = pwd.getpwuid(os.getuid()).pw_name
    except ImportError:
        username = os.environ.get("USERNAME")
    return username


def _get_db_connection_string():
    """Returns connection string to use.

    """
    def get_user_connection_string():
        result = None
        username = _get_user_name()
        if username == u"markmorgan":
            result = u"postgresql://postgres:Silence107!@localhost:5432/esdoc_api"
        elif username == u"cgam":
            result = u"postgresql://postgres:TORNADO1@localhost:5432/esdoc_api"
        return result

    # If the user has specified a connection string then use that otherwise revert to the default.
    user_specific = get_user_connection_string()
    if user_specific is not None:
        return user_specific
    else:
        return u"postgresql://postgres:Silence107!@localhost:5432/esdoc_api"


# Set engine.
metadata.bind = _get_db_connection_string()
metadata.bind.echo = False

# Set logging.
logging.basicConfig()
logging.getLogger('sqlalchemy.dialects').setLevel(logging.NOTSET)
logging.getLogger('sqlalchemy.engine').setLevel(logging.NOTSET)
logging.getLogger('sqlalchemy.orm').setLevel(logging.NOTSET)
logging.getLogger('sqlalchemy.pool').setLevel(logging.NOTSET)

# Set ORM.
setup_all()


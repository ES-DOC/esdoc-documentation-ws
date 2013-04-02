import elixir
from elixir import *

from esdoc_api.models import meta
from esdoc_api.lib.controllers.cache_data import *
from esdoc_api.lib.site import *

Session = elixir.session = meta.Session
metadata = elixir.metadata


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine

    elixir.session.configure(bind=engine)
    metadata.bind = engine

    # Create logical db objects.
    setup_all()

    
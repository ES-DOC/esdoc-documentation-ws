"""
.. module:: esdoc_api.config.routing
   :platform: Unix, Windows
   :synopsis: Encapsulates setting up URL to controller routing patterns.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

from routes import Mapper


def _make_map_for_common(map, config):
    """Constructs routing tables for common routes.

    :param map: Routes url map being constructed.
    :param config: Pylons configuration object.
    :type map: routes.PylonsConfig
    :type config: pylons.configuration.PylonsConfig

    """
    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')


def _make_map_for_api(map, config):
    """Constructs routing tables for web service api.

    :param map: Routes url map being constructed.
    :param config: Pylons configuration object.
    :type map: routes.PylonsConfig
    :type config: pylons.configuration.PylonsConfig

    """
    def publish():
        """Publish API routes.

        """
        if 'publishing_enabled' in config and bool(config['publishing_enabled']):
            map.connect('/1/publish/{project}',
                        controller='publish', action='collection')
            map.connect('/1/publish/{project}/{uid}/{version:\d+|latest|all}{.format:xml|json}',
                        controller='publish', action='instance')

    def search():
        """Search API routes.

        """
        map.connect('/1/search', controller='search', action='do')
        map.connect('/1/search/results', controller='search', action='results')
        map.connect('/1/search/setup', controller='search', action='setup')

        
    for f in [publish, search]:
        f()


def _make_map_for_frontend(map, config):
    """Constructs routing tables for front end.

    :param map: Routes url map being constructed.
    :param config: Pylons configuration object.
    :type map: routes.PylonsConfig
    :type config: pylons.configuration.PylonsConfig

    """
    # DEFAULT routes:
    map.connect('/', controller='frontend', action='info')
    map.connect('/index', controller='frontend', action='info')
    map.connect('/home', controller='frontend', action='info')

    # AJAX routes:
    map.connect('/frontend/ajax/{action}', controller='ajax')

    # PAGE routes:
    map.connect('/frontend', controller='frontend', action='info')
    map.connect('/frontend/public/about', controller='frontend', action='info')
    map.connect('/frontend/public/ingestion', controller='frontend', action='ingest_history')

    # DEFAULT routes:
    map.connect('/frontend/public/{controller}/{action}')


def make_map(config):
    """Creates, configures and returns the routes mapper.

    :param config: Pylons configuration object.
    :type config: pylons.configuration.PylonsConfig

    """
    # Instantiate mapper from config.
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # Create routing tables.
    mapppings = [
        _make_map_for_common,
        _make_map_for_frontend,
        _make_map_for_api
    ]
    for mapping in mapppings:
        mapping(map, config)

    return map

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
            map.connect('/1/publish/{project}/{uid}/{version:\d+|latest}{.format:xml|json}',
                        controller='publish', action='instance')

    def query():
        """Query API routes.

        """
        # Document - by id.
        map.connect('/1/query/id/{project_code}/{id}{.format:xml|json}',
                    controller='query', action='document_by_id')
        map.connect('/1/query/id/{project_code}/{id}/{version:\d+|latest}{.format:xml|json}',
                    controller='query', action='document_by_id')

        # Document - by name.
        map.connect('/1/query/name/{project_code}/{type}/{name}{.format:xml|json}',
                    controller='query', action='document_by_name')
        map.connect('/1/query/name/{project_code}/{type}/{name}/{institute_code}{.format:xml|json}',
                    controller='query', action='document_by_name')

        # Document - by external id.
        map.connect('/1/query/externalID/{project_code}/{type}/{external_id}{.format:xml|json}',
                    controller='query', action='document_by_external_id')

        # Document - by drs.
        path = '{project_code}'
        for i in range(9):
            if i > 0:
                path += '/{key_0' + str(i) + '}'
            map.connect('/1/query/drs/{0}{1}'.format(path, '{.format:xml|json}'),
                        controller='query', action='document_by_drs_keys')

    def repository():
        """Repository API routes.

        """
        # Setup data.
        map.connect('/1/repository/search/{search_type}/setupData',
                    controller='repository', action='get_search_setup_data')

        # Results.
        map.connect('/1/repository/search/{search_type}/results',
                    controller='repository', action='get_search_results')

    def compare():
        """Compare API routes.
        
        """
        # Setup data.
        map.connect('/1/compare/setupData/{project_code}/{comparator_type}',
                    controller='comparator', action='get_setup_data')


    def visualize():
        """Visualize API routes.

        """
        # Setup data.
        map.connect('/1/visualize/setupData/{visualizer_type}/{project_code}',
                    controller='visualizer', action='get_setup_data')


    for f in [publish, query, repository, compare, visualize]:
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

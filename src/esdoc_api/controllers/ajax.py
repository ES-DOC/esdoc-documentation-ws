"""
.. module:: esdoc_api.controllers.ajax
   :platform: Unix, Windows
   :synopsis: Encapsulates front-end ajax operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.models.core.entity_manager import EntityManager
from esdoc_api.models.core.entity_convertor import EntityConvertor
from esdoc_api.models.core.search_manager import SearchManager
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.lib.controllers import *
from esdoc_api.lib.controllers.decorators import jsonify
from esdoc_api.models.entities.types import *



class AjaxController(BaseSiteAjaxController):
    """ESDOC API ajax controller.

    """

    def get_search_results(self):
        """Returns search results based on the passed criteria.

        :returns: List of matching search results.
        :rtype: list
        
        """
        # Get type.
        type = get_search_type(request.params['searchType'])
        
        print "AJAX CONTROLLER - GET SEARCH RESULTS - {0}".format(type)

        # Instantiate search manager.
        user_session = {}
        manager = SearchManager(type,
                                request.params,
                                user_session,
                                auto_search=True)

        # Assign results / handler to response context.
        c.search_results = manager.results
        c.search_handler = manager.handler

        # Render.
        template = '/ajax/search-{0}-results.xhtml'.format(manager.type_key)
        return render(template)


    #@beaker_cache(type='memory', query_args=True)
    def get_search_criteria_form(self):
        """Returns an xhtml form for entering search criteria.

        :returns: An xhtml form for entering search criteria.
        :rtype: html
        
        """
        # Get type.
        type = get_search_type(request.params['searchType'])

        print "AJAX CONTROLLER - GET SEARCH CRITERIA FORM - {0}".format(type)

        # Instantiate manager.
        manager = SearchManager(type)

        # Render.
        template = '/ajax/search-{0}-criteria.xhtml'.format(manager.type_key)
        return render(template)


    @beaker_cache(type='memory', query_args=True)
    def get_entity_detail_form(self):
        """Returns an xhtml form for viewing/editing entity details.

        :returns: An xhtml form for viewing/editing entity details.
        :rtype: html

        """
        # Get type.
        type = request.params['entityType']

        print "AJAX CONTROLLER - GET ENTITY DETAIL FORM - {0}".format(type)

        # Render.
        template = '/ajax/entity-{0}.xhtml'.format(type.lower())
        return render(template)


    @jsonify
    def get_entity(self):
        """Retrieves an instance from the repository.

        :returns: JSON representation of an entity instance.
        :rtype: json
        
        """
        # Get type / id.
        type = get_entity_type(request.params['entityType'])
        id = request.params['entityID']

        print "AJAX CONTROLLER - GET ENTITY - {0} - {1}".format(type, id)

        # Instantiate manager.
        manager = EntityManager(type, instance_id=id)

        # Return instance.
        return EntityConvertor.to_dict(manager.instance)


    @jsonify
    def get_entity_collection(self):
        """Retrieves a collection of instances from the repository.

        :returns: JSON representation of an entity collection.
        :rtype: json

        """
        # Get type.
        type = get_entity_type(request.params['entityType'])

        print "AJAX CONTROLLER - GET ENTITY COLLECTION - {0}".format(type)

        # Instantiate manager.
        manager = EntityManager(type,
                                load_instance=False,
                                load_collection=True)

        # Return instance.
        return EntityConvertor.to_dict(manager.collection)


    def delete_entity(self):
        """Deletes an instance from the repository.
        
        """
        # Get type / id.
        type = get_entity_type(request.params['entityType'])
        id = request.params['entityID']
        
        print "AJAX CONTROLLER - DELETE ENTITY - {0} - {1}".format(type, id)

        # Instantiate manager.
        manager = EntityManager(type, id)

        # Delete instance.
        manager.delete_instance(session)


    @jsonify
    def save_entity(self):
        """Saves entity changes to the the repository.

        :returns: JSON representation inserted entity id/type.
        :rtype: json
        
        """
        # Get type / id / entity.
        type = get_entity_type(request.params['entityType'])
        id = request.params['entityID']
        entity = request.params['entity']

        print "AJAX CONTROLLER - SAVE ENTITY - {0} - {1}".format(type, id)

        # Instantiate manager.
        manager = EntityManager(type, instance_id=id, instance_json=entity)

        # Save instance.
        manager.save_instance(session)

        # Return new entity id.
        return { "entityType" : type, \
                 "entityID" : manager.instance.ID}


    @jsonify
    def get_collection(self):
        """Returns a collection from the cache.

        :returns: JSON representation of an entity collection.
        :rtype: json
        
        """
        key = request.params['cacheKey'].upper()
        # TODO implement as required.
        raise Exception(u'Unsupported cache key :: {0}'.format(key))


    @beaker_cache(type='memory', query_args=True, expire=3600)
    def __load_data(self, key):
        """ Loads a dynamic collection from backend.

        :param key: Cache item key.
        :type key: str
        :returns: Cached data.
        :rtype: object

        """
        # TODO add support for cached data retrieval as and when required.
        raise Exception(u'Unsupported cache key :: {0}'.format(key))


    @jsonify
    def get_data(self):
        """Returns data from server for use in client side.
        
        """
        # Get cache key.
        key = request.params['key'].upper()
        
        print "CACHE - GET DATA - {0}".format(key)

        # TODO add support for cached data retrieval as and when required.
        raise Exception(u'Unsupported data key :: {0}'.format(key))

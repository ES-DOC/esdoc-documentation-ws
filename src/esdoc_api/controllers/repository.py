"""
.. module:: pyesdoc_api.controllers.repository
   :platform: Unix, Windows
   :synopsis: Encapsulates common repository operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.models.core.entity_convertor import EntityConvertor
from esdoc_api.models.core.search_manager import SearchManager
from esdoc_api.models.types import get_type



class RepositoryController(BaseAPIController):
    """CIM repository comparator controller.

    """
    @property
    def validate_cim_info(self):
        """Gets flag indicating whether cim http request information should be validated or not.
        
        """
        return False


    def __to_dict(self, target):
        """Converts target to a dictionary.

        :param target: Either a function pointer, pre-loaded object or pre-loaded collection.
        :type target: func | object | list

        """        
        if hasattr(target, '__call__'):
            target = target()

        if isinstance(target, list):
            convert = len(target) > 0 and hasattr(target[0], 'as_dict')
        else:
            convert = hasattr(target, 'as_dict')

        return target if convert == False else EntityConvertor.to_dict(target)


    @rest.restrict('GET')
    @jsonify
    def get_search_setup_data(self, search_type):
        """Returns search setup data.

        :param search_type: Type of search, e.g. s1.
        :type search_type: str

        :returns: search setup data.
        :rtype: json object

        """
        print "REPOSITORY - GET SEARCH SETUP DATA - {0}".format(search_type)

        result = {
            'searchType' : search_type
        }

        if search_type == 's1':
            result['data'] = {
                'projects' : self.__to_dict(Project.retrieve_all),
                'documentTypes' : self.__to_dict(DocumentType.retrieve_all),
                'documentLanguages' : self.__to_dict(DocumentLanguage.retrieve_all),
                'results' : []
            }

        return result


    @rest.restrict('GET')
    @jsonify
    def get_search_results(self, search_type):
        """Returns search results.

        """
        print "REPOSITORY - GET SEARCH RESULTS - {0}".format(search_type)

        # Instantiate search manager.
        manager =  SearchManager(get_type(search_type + 'Search'), request.params)

        # Execute search.
        manager.execute()

        # Return.
        return {
            'searchType' : search_type,
            'results' : self.__to_dict(manager.results)
        }

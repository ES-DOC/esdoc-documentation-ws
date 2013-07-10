"""
.. module:: esdoc_api.controllers.query
   :platform: Unix, Windows
   :synopsis: Encapsulates repository query operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import itertools

from pylons.decorators import rest

from esdoc_api.lib.api.external_id import get_handler as get_external_id_handler
from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils


# Set of supported search types.
_SEARCH_TYPES = [
    'documentByID',
    'documentByName',
    'documentByExternalID',
    'documentByDRS'
]


class SearchController(BaseAPIController):
    """ES-DOC API repository query controller.

    """
    def __load_representation(self, document):
        """Loads a document representation.

        :param document: document being loaded.
        :type document: esdoc_api.lib.repo.models.Document

        :returns: A document representation.
        :rtype: str

        """
        return utils.get_document_representation(document,
                                                 self.ontology,
                                                 self.encoding,
                                                 self.language)


    def __load_representation_set(self, document_set):
        """Loads a document representation set.

        :param document_set: document set being loaded.
        :type document_set: array of documents.

        :returns: array of document representations.
        :rtype: string list

        """
        representation_set = []
        if document_set is not None:
            representation_set = [self.__load_representation(d) for d in document_set]
            
        return [r for r in representation_set if r is not None]


    def __load_children(self, document_set):
        """Loads child documents from repository.

        :param document_set: Set of documents being processed.
        :type document_set: list

        :returns: a document collection.
        :rtype: list Document

        """
        if (len(document_set) > 0):
            iterator = itertools.islice(document_set, 0, len(document_set))
            for document in iterator:
                if document.HasChildren:
                    document_set.extend(dao.get_document_sub_documents(document.ID))
                
        return document_set
    

    def __load(self, load):
        """Loads document representations from repository.

        :param load: Function to load document.
        :type load: Function

        :returns: A list of document representations.
        :rtype: list
        
        """
        # Set document set.
        document_set = load()
        if document_set is None:
            document_set = []
        elif isinstance(document_set, Document):
            document_set = [document_set]

        # Set sub documents.
        if (len(document_set) > 0):
            document_set = self.__load_children(document_set)

        # Set representations.
        if (len(document_set) > 0):
            document_set = self.__load_representation_set(document_set)

        # Set response content type.
        response.content_type = self.get_response_content_type()

        return document_set


    def __document_by_id(self):
        """Returns first document set with matching id and version.

        :returns: a collection of document representations.
        :rtype: json list

        """
        # Defensive programming.
        if not request.params.has_key('id'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter id is mandatory")

        if not request.params.has_key('version'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version is mandatory")
        
        if request.params['version'] not in ["latest", "all"]:
            try:
                int(request.params['version'])
            except ValueError:
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version must be either an integer or one of the string literals 'latest' | 'all'.")

        # Load document set.
        return self.__load(lambda : dao.get_document(self.project_id,
                                                     request.params['id'],
                                                     request.params['version']))


    def __document_by_name(self):
        """Returns first document set with matching type and name.

        :returns: a collection of document representations.
        :rtype: json list

        """
        # Defensive programming.
        if not request.params.has_key('type'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter type is mandatory")

        if not request.params.has_key('name'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter name is mandatory")
            
        # Load document set.        
        return self.__load(lambda : dao.get_document_by_name(self.project_id,
                                                             request.params['type'],
                                                             request.params['name'],
                                                             self.institute_id))


    def __document_by_drs(self):
        """Returns first document set with matching drs path.

        :returns: a set of document representations.
        :rtype: json list

        """
        # Defensive programming.
        if not request.params.has_key('drsPath'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter drsPath is mandatory")

        if len(request.params['drsPath'].split('/')) > 8:
            abort(HTTP_RESPONSE_BAD_REQUEST, "A DRS path must consist of a maximum 8 keys")
        
        # Format drs keys.
        keys = [x for x in request.params['drsPath'].split('/') if len(x) > 0]
        keys = [x for x in keys if not x.upper() == self.project.Name]

        # Load document set.
        return self.__load(lambda : dao.get_document_by_drs_keys(self.project_id,
                                                                 keys[0] if len(keys) > 0 else None,
                                                                 keys[1] if len(keys) > 1 else None,
                                                                 keys[2] if len(keys) > 2 else None,
                                                                 keys[3] if len(keys) > 3 else None,
                                                                 keys[4] if len(keys) > 4 else None,
                                                                 keys[5] if len(keys) > 5 else None,
                                                                 keys[6] if len(keys) > 6 else None,
                                                                 keys[7] if len(keys) > 7 else None))



    def __document_by_external_id(self):
        """Returns first document set with matching external type and id.

        :returns: a collection of document representations.
        :rtype: json list

        """
        # Defensive programming.
        if not request.params.has_key('externalID'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter externalID is mandatory")

        if not request.params.has_key('externalType'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter externalType is mandatory")

        handler = get_external_id_handler(self.project, request.params['externalType'])
        if handler is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, "External type is unsupported")

        if not handler.is_valid(request.params['externalID']):
            abort(HTTP_RESPONSE_BAD_REQUEST, "External ID is invalid")

        # Parse external id.
        external_id = handler.parse(request.params['externalID'])

        # Load document set.
        return self.__load(lambda : handler.do_query(self.project, external_id))


    @rest.restrict('GET')
    @jsonify
    def do(self):
        """Executes a search against ES-DOC API repository.

        """
        # Defensive programming.
        if self.is_doc_metainfo_valid == False:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'URL parameters {project}, {encoding}, {schema} & {language} are mandatory')

        if not request.params.has_key('searchType'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter {searchType} is mandatory")

        if not request.params['searchType'] in _SEARCH_TYPES:
            abort(HTTP_RESPONSE_BAD_REQUEST, "Search type is unsupported")

        # Set of search handlers.
        handlers = {
            'documentByDRS' : self.__document_by_drs,
            'documentByID' : self.__document_by_id,
            'documentByName' : self.__document_by_name,
            'documentByExternalID' : self.__document_by_external_id
        }

        # Return handler invocation result.
        return handlers[request.params['searchType']]()


    @rest.restrict('GET')
    @jsonify
    def setup(self):
        """Returns setup data used to configure a UI for searching against ES-DOC API repository.

        """
        # Defensive programming.
        if not request.params.has_key('searchType'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter {searchType} is mandatory")

        if not request.params['searchType'] in _SEARCH_TYPES:
            abort(HTTP_RESPONSE_BAD_REQUEST, "Search type is unsupported")

        # Initialise result.
        result = {
            'searchType' : request.params['searchType']
        }

        if search_type == 's1':
            result['data'] = {
                'projects' : self.__to_dict(dao.get_all(Project)),
                'documentTypes' : self.__to_dict(dao.get_all(DocumentType)),
                'documentLanguages' : self.__to_dict(dao.get_all(DocumentLanguage)),
                'results' : []
            }

        return result
        

    def __results(self):
        """Returns search results.

        """
        # TODO replace do operation with this style of code.
        # TODO move get search setup data to search manager / handler.
        # Instantiate search manager.
        manager =  SearchManager(get_type(search_type + 'Search'), request.params)

        # Execute search.
        manager.execute()

        # Return.
        return {
            'searchType' : search_type,
            'results' : self.__to_dict(manager.results)
        }


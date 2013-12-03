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
import esdoc_api.lib.api.search as se
import esdoc_api.lib.repo.cache as cache
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.models as models
import esdoc_api.lib.controllers.url_validation as uv



# Default URL query parameters.
_default_params = (
    {
        'name' : 'onJSONPLoad',
        'required' : False,
    },
    {
        'name' : 'project',
        'required' : True,
        'whitelist' : lambda : cache.get_names('Project'),
        'key_formatter' : lambda n : n.lower(),
    },
    {
        'name' : 'timestamp',
        'required' : True,
    },
    {
        'name' : 'searchType',
        'required' : True,
        'whitelist' : lambda : [
            'documentByDRS',
            'documentByExternalID',
            'documentByID',
            'documentByName',
            'documentSummaryByName',
            'se1',
        ],
    },
)

_params_do_defaults_document_by = _default_params + (
    {
        'name' : 'language',
        'required' : True,
        'whitelist' : lambda : cache.get_names('DocumentLanguage', 'Code'),
        'key_formatter' : lambda k : k.lower(),
    },
    {
        'name' : 'encoding',
        'required' : True,
        'whitelist' : lambda : cache.get_names('DocumentEncoding', 'Encoding'),
        'key_formatter' : lambda k : k.lower(),
    },
    {
        'name' : 'ontology',
        'required' : True,
        'whitelist' : lambda : cache.get_names('DocumentOntology'),
        'key_formatter' : lambda k : k.lower(),
    }
)

# URL query parameters for do action.
_params_do = {
    'documentByDRS' : _params_do_defaults_document_by + (
        {
            'name' : 'drsPath',
            'required' : True
        },
    ),
    'documentByExternalID' : _params_do_defaults_document_by + (
        {
            'name' : 'externalID',
            'required' : True,
        },
        {
            'name' : 'externalType',
            'required' : True,
        },
        {
            'name' : 'typeWhiteList',
            'required' : False,
        },
        {
            'name' : 'typeBlackList',
            'required' : False,
        },
    ),
    'documentByID' : _params_do_defaults_document_by + (
        {
            'name' : 'id',
            'required' : True,
        },
        {
            'name' : 'version',
            'required' : True,
        },
    ),
    'documentByName' : _params_do_defaults_document_by + (
        {
            'name' : 'name',
            'required' : True,
        },
        {
            'name' : 'type',
            'required' : True,
        },
        {
            'name' : 'institute',
            'required' : False,
            'whitelist' : lambda : cache.get_names('Institute'),
            'key_formatter' : lambda k : k.lower(),
        },
    ),
    'documentSummaryByName' : _default_params + (
        
    ),
    'se1' : _default_params + (
        {
            'name' : 'documentLanguage',
            'required' : True,
            'whitelist' : lambda : cache.get_names('DocumentLanguage', 'Code'),
            'key_formatter' : lambda k : k.lower(),
        },
        {
            'name' : 'documentType',
            'required' : True,
            'whitelist' : lambda : cache.get_names('DocumentType', 'Key'),
            'key_formatter' : lambda k : k.lower(),
        },
        {
            'name' : 'documentVersion',
            'required' : True,
            'whitelist' : lambda : models.DOCUMENT_VERSIONS
        },
        {
            'name' : 'institute',
            'required' : False,
            'whitelist' : lambda : cache.get_names('Institute'),
            'key_formatter' : lambda k : k.lower(),
        }
    )
}


# URL query parameters for setup action.
_params_setup = {
    'se1' : _default_params
}


def _validate_url_params(params):
    """Helper method to validate url parameters."""
    # Validate search type.
    uv.validate(_default_params[2])

    # Validate other params.
    uv.validate(params[request.params['searchType']])


def _get_se_params():
    """Factory method to derive set of search engine parameters from url."""
    params = {}
    for key in [k for k in request.params if k not in ('onJSONPLoad', 'searchType')]:
        params[key] = request.params[key]

    return params


class SearchController(BaseAPIController):
    """ES-DOC API repository query controller.

    """
    def __before__(self, action, **kwargs):
        """Pre action invocation handler.

        """
        super(SearchController, self).__before__(action, **kwargs)

        # Set common context info.
        self.__set_doc_metainfo()


    def __set_doc_metainfo(self):
        """Assigns document meta-information from incoming http request.

        """
        # Assign values.
        setters = [
            self.__set_doc_project,
            self.__set_doc_institute,
            self.__set_doc_ontology,
            self.__set_doc_encoding,
            self.__set_doc_language
        ]
        for setter in setters:
            setter()


    def __set_doc_project(self):
        """Assigns document project from incoming http request.

        """
        self.project = None if not request.params.has_key('project') else \
                       cache.get_project(request.params['project'])
        self.project_id = None if self.project is None else self.project.ID


    def __set_doc_institute(self):
        """Assigns document institute from incoming http request.

        """
        self.institute = None if not request.params.has_key('institute') else \
                         cache.get_institute(request.params['institute'])
        self.institute_id = None if self.institute is None else self.institute.ID


    def __set_doc_encoding(self):
        """Assigns document encoding from incoming http request.

        """
        self.encoding = None if not request.params.has_key('encoding') else \
                        cache.get_doc_encoding(request.params['encoding'])
        self.encoding_id = None if self.encoding is None else self.encoding.ID


    def __set_doc_language(self):
        """Assigns document language from incoming http request.

        """
        self.language = None if not request.params.has_key('language') else \
                        cache.get_doc_language(request.params['language'].split('-')[0].lower())
        self.language_id = None if self.language is None else self.language.ID


    def __set_doc_ontology(self):
        """Assigns document ontology from incoming http request.

        """
        self.ontology = None if not request.params.has_key('ontology') else \
                        cache.get_doc_ontology(request.params['ontology'])
        self.ontology_id = None if self.ontology is None else self.ontology.ID


    def __load_representation(self, document):
        """Loads a document representation.

        :param document: document being loaded.
        :type document: esdoc_api.models.Document

        :returns: A document representation.
        :rtype: str

        """
        return utils.get_doc_representation(document,
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


    def __apply_type_filters(self, ds):
        """Apply white/black type list filters."""
        def apply_type_filter(param):
            type_keys = map(lambda s : s.strip(),
                            request.params[param].upper().split(','))
            is_white_list = True if 'White' in param else False
            def do_filter(memo, d):
                if is_white_list:
                    if d.Type.upper() in type_keys:
                        memo.append(d)
                elif d.Type.upper() not in type_keys:
                    memo.append(d)
                return memo

            return reduce(do_filter, ds, [])

        for param in ['typeBlackList', 'typeWhiteList']:
            if request.params.has_key(param):
                ds = apply_type_filter(param)

        return ds


    def __initialise_ds(self, ds):
        if ds is None:
            ds = []
        elif isinstance(ds, Document):
            ds = [ds]

        return ds

    def __load(self, load):
        """Loads document representations from repository.

        :param load: Function to load document.
        :type load: Function

        :returns: A list of document representations.
        :rtype: list
        
        """
        # Apply transformations.
        transformations = [
            self.__initialise_ds,
            self.__load_children,
            self.__apply_type_filters,
            self.__load_representation_set
        ]
        return reduce(lambda ds, f : f(ds), transformations, load())
    

    def __get_documentset_by_id(self):
        """Returns first document set with matching id and version.

        :returns: a collection of document representations.
        :rtype: json list

        """
        # Defensive programming.
        if not request.params.has_key('id'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter id is mandatory")

        if not request.params.has_key('version'):
            abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version is mandatory")
        
        if request.params['version'] not in models.DOCUMENT_VERSIONS:
            try:
                int(request.params['version'])
            except ValueError:
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version must be either an integer or one of the string literals 'latest' | '*'.")

        # Load document set.
        return self.__load(lambda : dao.get_document(self.project_id,
                                                     request.params['id'],
                                                     request.params['version']))


    def __get_documentset_by_name(self):
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


    def __get_documentset_by_drs(self):
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



    def __get_documentset_by_external_id(self):
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


    def __load_results(self):
        """Returns search engine results.

        """
        try:
            searchType = request.params['searchType']
            params = _get_se_params()
            return se.get_results_data(searchType, params)
        except rt.ESDOC_API_Error as e:
            abort(HTTP_RESPONSE_BAD_REQUEST, e.message)


    def __load_setup(self):
        """Returns search engine setup data.

        """
        try:
            searchType = request.params['searchType']
            project = request.params['project']
            return se.get_setup_data(searchType, project)
        except rt.ESDOC_API_Error as e:
            abort(HTTP_RESPONSE_BAD_REQUEST, e.message)


    @rest.restrict('GET')
    @jsonify
    def do(self):
        """Executes a document set search against ES-DOC API repository.

        """
        # Validate URL query parameters.
        _validate_url_params(_params_do)

        # Set of handlers.
        handlers = {
            'documentByDRS' : self.__get_documentset_by_drs,
            'documentByID' : self.__get_documentset_by_id,
            'documentByName' : self.__get_documentset_by_name,
            'documentByExternalID' : self.__get_documentset_by_external_id,
            'documentSummaryByName' : self.__load_results,
            'se1' : self.__load_results,
        }

        # Set response content type.
        response.content_type = self.get_response_content_type()

        # Return handler invocation result.
        return handlers[request.params['searchType']]()


    @rest.restrict('GET')
    @jsonify
    def setup(self):
        """Returns setup data used to configure a UI for searching against ES-DOC API repository.

        :returns: Search engine setup data.
        :rtype: dict

        """
        # Validate URL query parameters.
        _validate_url_params(_params_setup)

        # Set of handlers.
        handlers = {
            'se1' : self.__load_setup,
        }

        # Return handler invocation result.
        return handlers[request.params['searchType']]()
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
from esdoc_api.lib.pyesdoc.ontologies.constants import *
from esdoc_api.models.daos.document_representation import load as load_representation



class QueryController(BaseAPIController):
    """CIM repository query controller.

    """
    @property
    def validate_doc_request_info(self):
        """Gets flag indicating whether http request should be validated to ensure that cim information is specified correctly.

        """
        return True


    def __abort(self, http_code, msg):
        """Aborts request processing.

        :param http_code: HTTP error code.
        :param msg: Request processing error message.
        :type http_code: str
        :type msg: str

        """
        msg = 'WARNING :: Bad CIM API Query request - {0}'.format(msg)
        abort(http_code, msg)


    def __load_project(self, code):
        """Loads project cvocab in readiness for subsequent actions.

        :param code: The project code, e.g. CMIP5.
        :type code: str

        :returns: A project instance.
        :rtype: models.entity.Project

        """
        # 400 if parameters are invalid.
        if code is None:
            self.__abort(HTTP_RESPONSE_BAD_REQUEST, 'Project code is unspecified')

        # Load from cache.
        project = c.get_project(code)

        # 406 if not found.
        if project is None:
            self.__abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Project code ({0}) is unsupported'.format(code))

        return project


    def __load_institute(self, code):
        """Loads institute cvocab in readiness for subsequent actions.

        :param code: The institute code, e.g. IPSL.
        :type code: str

        :returns: An institute instance.
        :rtype: models.entity.Institute

        """
        # 400 if parameters are invalid.
        if code is None:
            self.__abort(HTTP_RESPONSE_BAD_REQUEST, 'Institute code is unspecified')

        # Load from cache.
        institute = c.get_institute(code)

        # 406 if not found.
        if institute is None:
            self.__abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Institute code ({0}) is unsupported'.format(code))

        return institute


    def __load_representation(self, document):
        """Loads a document representation.

        :param doc: document being loaded.
        :type doc: Document -- a document instance.

        :returns: a document representation.
        :rtype: string

        """
        return load_representation(document,
                                   self.cim_schema,
                                   self.cim_encoding,
                                   self.cim_language)


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
                    document_set.extend(Document.retrieve_children(document))

        return document_set
    

    def __load(self, project_code, load):
        """Loads document representations from repository.

        :param project_code: The project code, e.g. CMIP5.
        :param load: Function to load document.
        :type project_code: str
        :type load: Function

        :returns: A list of document representations.
        :rtype: list
        
        """
        # Abort if cim info is invalid.
        if self.is_cim_info_valid == False:
            self.__abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Invalid cim encoding/schema/language info')

        # Set project code.
        project = self.__load_project(project_code)
        
        # Set document set.
        document_set = load(project)
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


    @rest.restrict('GET')
    @jsonify
    def document_by_id(self, project_code, id, version=None):
        """Returns document matched by project, id and version.

        :param project_code: The project code, e.g. CMIP5.
        :param id: Document identifier.
        :param version: Document version.
        :type project_code: str
        :type id: str
        :type version: str

        :returns: a collection of document representations.
        :rtype: json list

        """
        def load(project):
            return Document.retrieve_by_id(project, id, version)

        return self.__load(project_code, load)


    @rest.restrict('GET')
    @jsonify
    def document_by_name(self, project_code, type, name, institute_code=None):
        """Returns document matched by project, type and name.

        :param project_code: The project code, e.g. CMIP5.
        :param type: Document type.
        :param name: Document name.
        :param institute_code: Institute code.
        :type project_code: str
        :type type: str
        :type name: str
        :type institute_code: str

        :returns: a collection of document representations.
        :rtype: json list

        """
        def load(project):
            institute = None
            if institute_code is not None:
                institute = self.__load_institute(institute_code)
                
            retrieve = Document.retrieve_by_name
            return retrieve(project, type, name, institute)

        return self.__load(project_code, load)


    @rest.restrict('GET')
    @jsonify
    def document_by_drs_keys(self,
                             project_code,
                             key_01=None,
                             key_02=None,
                             key_03=None,
                             key_04=None,
                             key_05=None,
                             key_06=None,
                             key_07=None,
                             key_08=None):
        """Returns document matched by project, drs keys.

        :param project_code: The project code, e.g. CMIP5.
        :param key_01: DRS key 1.
        :param key_02: DRS key 2.
        :param key_03: DRS key 3.
        :param key_04: DRS key 4.
        :param key_05: DRS key 5.
        :param key_06: DRS key 6.
        :param key_07: DRS key 7.
        :param key_08: DRS key 8.
        :type project_code: str
        :type key_01: str
        :type key_02: str
        :type key_03: str
        :type key_04: str
        :type key_05: str
        :type key_06: str
        :type key_07: str
        :type key_08: str

        :returns: a set of document representations.
        :rtype: json list

        """
        def load(project):
            return Document.retrieve_by_drs_keys(project,
                                                 key_01,
                                                 key_02,
                                                 key_03,
                                                 key_04,
                                                 key_05,
                                                 key_06,
                                                 key_07,
                                                 key_08)

        return self.__load(project_code, load)


    @rest.restrict('GET')
    @jsonify
    def document_by_external_id(self, project_code, type, external_id):
        """Returns document matched by project, external id type, external id.

        :param project_code: The project code, e.g. CMIP5.
        :param type: Type of external id.
        :param id: Document set external identifer.
        :type project_code: str
        :type type: str
        :type id: str

        :returns: a collection of document representations.
        :rtype: json list

        """
        def load(project):
            # None if unsupported external id types.
            handler = get_external_id_handler(project, type)
            if handler is None:
                print 'WARNING :: Unsupported external ID type'
                return None

            # None if invalid external id types.
            if handler.is_valid(external_id) == False:
                print 'WARNING :: Invalid external ID'
                return None

            # Execute query over parsed id.
            return handler.do_query(project, handler.parse(external_id))

        return self.__load(project_code, load)


    @rest.restrict('GET')
    @jsonify
    def document_by_type(self, project_code, type, version_filter, language_code):
        """Returns document matched by project, type, version and language.

        :param project_code: The project code, e.g. CMIP5.
        :param type: Type of document, e.g. modelComponent.
        :param version_filter: All | Latest.
        :param language_code: Document language code.
        :type project_code: str
        :type type: str
        :type version_filter: All | Latest.
        :type language_code: str

        :returns: a collection of document summaries.
        :rtype: json list

        """
        pass
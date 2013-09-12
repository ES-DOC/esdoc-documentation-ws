"""
.. module:: esdoc_api.controllers.publish
   :platform: Unix, Windows
   :synopsis: Encapsulates document instance publishing operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.utils.runtime as rt



class PublishController(BaseAPIController):
    """Exposes document publishing operations.

    """
    def __load(self, project, uid, version):
        """Loads data in readiness for subsequent actions.

        :param project: A project code.
        :param uid: Document unique identifier.
        :param version: Document version.
        :type project: str
        :type uid: str
        :type version: str

        :returns: Matching project and document.
        :rtype: list
        
        """        
        # 400 if parameters are invalid.
        if project is None or uid is None or version is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Bad CIM document request')

        # Set default result.
        result = [None, None]

        # Load project (escape if not found).
        project = c.get_project(project)
        if project is None:
            return result
        result[1] = project

        # Load document.
        result[0] = dao.get_document(project_id, uid, version)

        # Returned loaded data.
        return result


    def __parse_xml(self):
        """Deconstructs request data in readiness for subsequent actions.

        :returns: List containing parsed document xml, id, version, type ann object.
        :rtype: list

        """
        doc_xml = request.body.decode('UTF-8','strict')
        doc_et = et.fromstring(doc_xml)
        doc_uid = get_element(doc_et, 'documentID').text
        doc_version = int(get_element(doc_et, 'documentVersion').text)
        doc_type = get_tag_name(doc_et)
        doc_obj = pyesdoc.decode(doc_xml, 'cim', '1', pyesdoc.ESDOC_ENCODING_XML)
        return [doc_xml, doc_uid, doc_version, doc_type, doc_obj]


    def __set_representations(self, doc, doc_xml, doc_obj):
        """Assign set of document representations.

        :param doc: Document.
        :param doc_xml: Document xml representation.
        :param doc_obj: Document object representation.
        :type doc: esdoc_api.models.Document
        :type doc_xml: lxml.etree
        :type doc_obj: object

        """
        self.__set_representation(doc, doc_obj, pyesdoc.ESDOC_ENCODING_JSON)
        self.__set_representation(doc, doc_obj, pyesdoc.ESDOC_ENCODING_XML,
                                  representation=doc_xml)


    def __set_representation(self, document, as_obj, encoding, representation=None):
        """Sets a document representation.

        :param document: Document.
        :type document: esdoc_api.models.Document

        :param as_obj: Document as a pyesdoc object.
        :type as_obj: object

        :param encoding: Document encoding.
        :type encoding: esdoc_api.models.DocumentEncoding

        :param representation: Document representation.
        :type representation: Document representation (e.g. xml | json).

        """
        # Deserialze pyesdoc object (if necessary).
        if representation is None:
            representation = pyesdoc.encode(as_obj,
                                            self.ontology.Name,
                                            self.ontology.Version,
                                            encoding)

        # Assign representation to document.
        utils.create_doc_representation(document,
                                             self.ontology,
                                             c.get_encoding(encoding),
                                             self.language,
                                             representation)

    
    def _instance_retrieve(self, project, uid, version):
        """Retrieves a document from repository.

        :param project: Document project code.
        :param uid: Document uid.
        :param version: Document version.
        :type project: str
        :type uid: str
        :type version: str

        :returns: Document representation.
        :rtype: unicode (utf-8)
        
        """
        def guard():
            # Abort if cim info is invalid.
            if self.is_doc_metainfo_valid == False:
                abort(HTTP_RESPONSE_NOT_ACCEPTABLE)

        # Defensive programming.
        guard()

        # Load from repository.
        doc, doc_project, = self.__load(project, uid, version)

        # Escape if either project or document is not found.
        if doc_project is None:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Unsupported project')
        if doc is None:
            abort(HTTP_RESPONSE_NOT_FOUND, 'CIM Document Not Found')

        # Load representation.
        representation = utils.get_doc_reprensentation(doc,
                                                           self.ontology,
                                                           self.encoding,
                                                           self.language)

        # Set response content type.
        response.content_type = self.get_response_content_type()

        # Log.
        rt.log('CIM Document retrieved :: {0} {1} {2} {3} {4} {5}'.format(
            project, self.ontology.Version, self.language.Code,
            self.encoding.Encoding, uid, version))

        # Return representation.
        return representation
    

    def _instance_delete(self, project, uid, version):
        """Deletes a document from repository.

        :param project: Document project code.
        :param uid: Document uid.
        :param version: Document version.
        :type project: str
        :type uid: str
        :type version: str

        """
        def guard():
            pass

        # Defensive programming.
        guard()

        # Load from repository.
        document, project = self.__load(project, uid, version)

        # Escape if either project or document is not found.
        if project is None:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, "Unsupported project")
        if document is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, "No matching CIM document.")

        # Delete relations.
        DocumentSetDocument.remove_all(document)
        dao.delete_document_representations(document.ID)
        dao.delete_document_summaries(document.id)
        dao.delete(document)

        # Log.
        rt.log("CIM Document deleted :: {0} {1} {2}".format(
            project, uid, version))


    def _instance_update(self, project, uid, version):
        """Updates a document within repository.

        :param project: Document project code.
        :param uid: Document uid.
        :param version: Document version.
        :type project: str
        :type uid: str
        :type version: str
        
        """
        def guard():
            # Abort if cim info is invalid.
            if self.is_doc_metainfo_valid == False:
                abort(HTTP_RESPONSE_NOT_ACCEPTABLE)

            # Abort if cim encoding is unacceptable.
            # TODO support other encodings.
            if self.encoding.Encoding != ESDOC_ENCODING_XML:
                abort(HTTP_RESPONSE_NOT_ACCEPTABLE)

        # Defensive programming.
        guard()

        # Parse request content.
        doc_xml, doc_uid, doc_version, doc_type, doc_obj = self.__parse_xml()

        # Load from repository.
        doc, doc_project = self.__load(project, doc_uid, doc_version)

        # Escape if either project or document is not found.
        if doc_project is None:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Unsupported project')
        if doc is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'CIM document does not exist.')

        # Update document core attributes.
        doc.Type = doc_obj.type_key

        # Update document summary.
        doc.set_summary(doc_obj, self.language)

        # Update document representations.
        self.__set_representations(doc, doc_xml, doc_obj)
        
        # Update document is latest flag.
        utils.set_doc_is_latest_flag(doc, doc_project)

        # Persist to db.
        session.commit()

        # Log.
        rt.log("CIM Document updated :: {0} {1} {2} {3} {4} {5} {6}".format(
            project, self.ontology.Version, self.language.Code,
            self.encoding.Encoding, doc_type, uid, version))

        # Return.
        response.content_type = 'text/xml'
        return doc_xml


    def _instance_create(self, project):
        """Appends an instance to the managed collection.

        :param project: Document project code.
        :type project: str
        
        """
        # Abort if document meta-info is invalid.
        if self.is_doc_metainfo_valid == False:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, "Invalid document meta-inforation")

        # Abort if document ontology is unacceptable.
        if self.ontology.Version != ontology_1_5:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, "Invalid document ontology")

        # Abort if document encoding is unacceptable.
        if self.encoding.Encoding != ESDOC_ENCODING_XML:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, "Invalid document encoding")

        # Parse request content.
        doc_xml, doc_uid, doc_version, doc_type, doc_obj = self.__parse_xml()

        # Load from repository.
        doc, doc_project = self.__load(project, doc_uid, doc_version)

        # Escape if project is not found or document already exists.
        if doc_project is None:
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, 'Unsupported project')
        if doc is not None:
            abort(HTTP_RESPONSE_NOT_ALLOWED, "Duplicate document")

        # Set document core attributes.
        doc = Document()
        doc.Project_ID = doc_project.ID
        doc.UID = doc_uid
        doc.Version = doc_version
        doc.Type = doc_obj.type_key

        # Set associated attributes.
        doc.set_summary(doc_obj, self.language)
        self.__set_representations(doc, doc_xml, doc_obj)
        utils.set_doc_is_latest_flag(doc, doc_project)

        # Persist to db.
        session.commit()

        # Log.
        rt.log("CIM Document uploaded :: {0} {1} {2} {3} {4} {5} {6}".format(
            project, self.ontology.Version, self.language.Code,
            self.encoding.Encoding, doc_type, doc_uid, doc_version))

        # Return.
        response.content_type = 'text/xml'
        return doc_xml
    

    @rest.dispatch_on(POST='_instance_create')
    def collection(self, project):
        """Processes requests to collection endpoint.

        :param project: Document project code.
        :type project: str
        
        """
        pass


    @rest.dispatch_on(GET='_instance_retrieve',
                      DELETE='_instance_delete',
                      PUT='_instance_update')
    def instance(self, project, uid, version):
        """Processes requests to instance endpoint.

        :param project: Document project code.
        :param uid: Document uid.
        :param version: Document version.
        :type project: str
        :type uid: str
        :type version: str
        
        """
        pass

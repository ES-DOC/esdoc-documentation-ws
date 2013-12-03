"""
.. module:: esdoc_api.controllers.publishing.py
   :platform: Unix, Windows
   :synopsis: Encapsulates document publishing operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest
from pylons import request
from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.xml_utils import *
import esdoc_api.lib.repo.cache as cache
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.utils.http_utils as http
import esdoc_api.models as models



def _exec(f):
    try:
        return f()
    except rt.ESDOC_API_Error as e:
        rt.log(e)
        abort(http.HTTP_RESPONSE_INTERNAL_SERVER_ERROR, e)


class PublishingController(BaseAPIController):
    """Exposes document publishing operations.

    """
    def _create(self):
        """Creates a document within repo."""
        def do():
            return utils.create_doc_from_json(request.body.decode('UTF-8','strict'))

        return _exec(do)


    def _delete(self, uid, version=None):
        """Delete document from repo."""
        def do():
            utils.delete_doc(uid, version)

        return _exec(do)

    
    def _retrieve(self, uid, version, format=pyesdoc.ESDOC_ENCODING_JSON):
        """Retrieves document from repo."""
        print "AAA", format
        def do():
            doc = dao.get_document(None, uid, version)
            if doc is not None:
                encoding = cache.get_doc_encoding(pyesdoc.ESDOC_ENCODING_JSON)
                language = cache.get_doc_language(pyesdoc.ESDOC_DEFAULT_LANGUAGE)
                ontology = cache.get_doc_ontology('cim', '1')                
                repr = dao.get_doc_representation(doc.ID, ontology.ID, encoding.ID, language.ID)
                if repr is not None:
                    if format == pyesdoc.ESDOC_ENCODING_JSON:
                        return repr.Representation
                    elif format == pyesdoc.ESDOC_ENCODING_XML:
                        return pyesdoc.convert(repr.Representation, pyesdoc.ESDOC_ENCODING_JSON, pyesdoc.ESDOC_ENCODING_XML)


            return None
        
        return _exec(do)            


    @rest.dispatch_on(POST='_create')
    @jsonify
    def collection(self):
        """Processes requests to collection endpoint.

        """
        pass


    @rest.dispatch_on(DELETE='_delete')
    @jsonify
    def instance(self, uid):
        """Processes requests to collection endpoint.

        :param uid: Document uid.
        :type uid: str

        """
        pass


    @rest.dispatch_on(GET='_retrieve', DELETE='_delete')
    @jsonify
    def version(self, uid, version, format=pyesdoc.ESDOC_ENCODING_JSON):
        """Processes requests to instance endpoint.

        :param uid: Document uid.
        :type uid: str
        
        :param version: Document version.
        :type version: str

        """
        pass



"""
.. module:: esdoc_api.controllers.publishing.py
   :platform: Unix, Windows
   :synopsis: Encapsulates document publishing operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.lib.pyesdoc as pyesdoc



class PublishingController(BaseAPIController):
    """Exposes document publishing operations.

    """
    def instance_create(self, uid, version):
        print "instance_create", uid, version

        return {
            type : "instance_create"
        }


    def instance_retrieve(self, uid, version):
        doc = dao.get_document(None, uid, version)
        if doc is not None:
            encoding = cache.get_document_encoding(pyesdoc.ESDOC_ENCODING_JSON)
            language = cache.get_document_language(pyesdoc.ESDOC_DEFAULT_LANGUAGE)
            ontology = cache.get_document_ontology('cim', '1')
            repr = dao.get_document_representation(doc.ID, ontology.ID, encoding.ID, language.ID)
            if repr is not None:
                return repr.Representation
        
        return None


    def instance_update(self, uid, version):
        print "instance_update", uid, version

        return {
            type : "instance_update"
        }

    def instance_delete(self, uid, version):
        print "instance_delete", uid, version

        return {
            type : "instance_delete"
        }


    def collection_retrieve(self, uid):
        print "instance_delete", uid

        return {
            type : "collection_retrieve"
        }


    @rest.dispatch_on(GET='collection_retrieve')
    @jsonify
    def collection(self, uid):
        """Processes requests to collection endpoint.

        :param uid: Document uid.
        :type uid: str

        """
        pass


    @rest.dispatch_on(GET='instance_retrieve',
                      POST='instance_create',
                      DELETE='instance_delete',
                      PUT='instance_update')
    @jsonify
    def instance(self, uid, version):
        """Processes requests to instance endpoint.

        :param uid: Document uid.
        :type uid: str
        
        :param version: Document version.
        :type version: str

        """
        pass

"""
Exposes management operations over the set of Prodiguer entities.
"""

# Module imports.
import simplejson
from StringIO import StringIO

from esdoc_api.models.core.entity_base import ESDOCEntity
from esdoc_api.lib.utils.exception import ESDOCAPIException



class EntityManager(object):
    """
    Exposes management operations over Prodiguer entities.
    """

    def __init__(self, type, load_instance=True, instance_id=None, instance_json=None, load_collection=False):
        """
        Constructor.
        """
        # Initialise members.
        self.__type = type
        self.__instance = None
        self.__instance_json = None
        self.__collection = None
        self.__collection_json = None

        # Validate type info.
        if self.__type is None:
            raise ESDOCAPIException("Entity type is unspecified.")
        if issubclass(self.__type, ESDOCEntity) == False:
            raise ESDOCAPIException("Entity type must derive from ESDOCAPIException.")

        # Load instance.
        if load_instance == True:
            self.__set_instance(instance_id, instance_json)

        # Load collection.
        if load_collection == True:
            self.__set_collection()



    @property
    def type(self):
        """The entity type."""
        return self.__type


    @property
    def instance(self):
        """The instance being managed."""
        return self.__instance


    @property
    def instance_json(self):
        """The json representation of instance being managed."""
        return self.__instance_json


    @property
    def collection(self):
        """The collection being managed."""
        return self.__collection


    def __set_instance(self, instance_id, instance_json):
        """Loads instance into memory."""

        # Either load from db or create new as appropriate.
        if instance_id is not None and int(instance_id) > 0:
            self.__instance = self.type.get_by_id(int(instance_id))
            if self.__instance is None:
                raise ProdiguerException("Entity does not exist :: {0} :: {1}".format(self.__type.__name__, instance_id))
        else:
            self.__instance = self.type()

        # Deserialize from json representation
        if instance_json is not None:
            io = StringIO(instance_json)
            self.__instance_json = simplejson.load(io)
            self.instance.from_dict(self.__instance_json)


    def __set_collection(self):
        """Loads collection into memory."""
        # Load from db.
        self.__collection = self.type.get_all()


    def delete_instance(self, session=None):
        """
        Deletes instance being managed.
        """
        # Exception if previously deleted.
        if self.__instance is None:
            raise ProdiguerException("Entity already deleted")

        # Delete & commit (if instructed).
        self.__instance.delete()
        if session is not None:
            session.commit()
            
        # Update state.
        self.__instance = None


    def save_instance(self, session=None):
        """
        Deletes instance being managed.
        """

        # Ensure instance ID is None for inserts.
        if self.__instance is not None and self.__instance.ID == 0:
            self.__instance.ID = None

        # Commit (if instructed).
        if session is not None:
            session.commit()

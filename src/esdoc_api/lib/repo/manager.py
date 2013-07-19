"""
.. module:: esdoc_api.models.manager.py
   :copyright: Copyright "Jun 27, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of model management classes.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import json
from StringIO import StringIO

import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.utils.runtime as rt



class EntityManager(object):
    """Exposes management operations over ES-DOC API entities.

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
            raise rt.ESDOC_API_Error("Entity type is unspecified.")
        if issubclass(self.__type, ESDOCEntity) == False:
            raise rt.ESDOC_API_Error("Entity type must derive from rt.ESDOC_API_Error.")

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
            self.__instance_json = json.load(io)
            self.instance.from_dict(self.__instance_json)


    def __set_collection(self):
        """Loads collection into memory."""
        # Load from db.
        self.__collection = dao.get_all(self.type)


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




class SearchContext(object):
    """Encapsulates search process contextual information.

    """
    def __init__(self, criteria):
        """Constructor.

        :param criteria: Search criteria.
        :type criteria: A subclass of models.core.ESDOCSearchCriteriaBase

        """
        self.c = criteria
        self.r = []
        self.q = None


    def set_join(self, expression):
        """Adds a join expression to query.

        :param expression: Join expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.join(expression)


    def set_filter(self, expression):
        """Adds a filter expression to query.

        :param expression: Filter expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.filter(expression)


    def set_sort(self, expression):
        """Adds a sort expression to query.

        :param expression: Sort expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.order_by(expression)


class SearchManager(object):
    """Encapsulates the management of search process.

    """

    def __init__(self, type, params=None):
        """Constructor.

        :param type: Type of search being executed.
        :param params: Search criteria.

        :type type: subclass of models.core.ESDOCSearchBase
        :type params: dict

        """
        # Defensive programming.
        if type is None:
            raise rt.ESDOC_API_Error("Search type is unspecified.")
        if issubclass(type, ESDOCSearchBase) == False:
            raise rt.ESDOC_API_Error("Search type must derive from models.core.ESDOCSearchBase.")

        # Initialise.
        self.handler = type()
        self.results = None
        self.criteria = self.handler.criteria_type()

        # Hydrate criteria.
        if params is not None:
            self.criteria.hydrate(params)


    def execute(self):
        """Executes search.

        """
        self.results = self.handler.do_search(self.criteria)


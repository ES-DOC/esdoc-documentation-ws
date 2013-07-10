"""
.. module:: esdoc_api.lib.repo.dao.core.py
   :platform: Unix
   :synopsis: Set of core repo data access operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.repo.models as models
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.runtime as rt


# Module exports.
__all__ = [
    'assert_type',
    'assert_collection',
    'delete',
    'delete_all',
    'delete_by_facet',
    'delete_by_id',
    'delete_by_name',
    'get_active',
    'get_all',
    'get_by_facet',
    'get_by_id',
    'get_by_name',
    'get_count',
    'get_inactive',
    'insert',
    'insert_all',
    'sort'
]



def assert_type(type):
    """Asserts that passed type is supported.

    :param type: A supported entity type.
    :type type: class

    """
    def get_msg():
        return "Unsupported model type ({0}).".format(type.__class__.__name__)

    rt.assert_iter_item(models.supported_types, type, get_msg)


def assert_instance(instance):
    """Asserts that passed instance is of a supported type.

    :param instance: An repo model instance being processed.
    :type instance: sub-class of models.Entity

    """
    assert_type(instance.__class__)


def assert_collection(collection):
    """Asserts that all members of the passed colllection are supported types.

    :param collection: A collection of supported entity types.
    :type collection: iterable

    """
    for instance in collection:
        assert_instance(instance)


def sort(type, collection):
    """Sorts collection via type sort key.

    :param type: A supported entity type.
    :type type: class

    :param collection: Collection of entities.
    :type collection: list

    :returns: Sorted collection.
    :rtype: list

    """
    # Defensive programming.
    assert_type(type)

    return [] if collection is None else type.get_sorted(collection)


def _get_active(type, is_active_state):
    """Gets instances filtered by their IsActive state.

    :param type: A supported entity type.
    :type type: class

    :param is_active_state: Entity IsActive field value.
    :type is_active_state: bool

    :returns: Entity collection.
    :rtype: list

    """
    # Defensive programming.
    assert_type(type)
    
    return get_by_facet(type, filter=type.IsActive==is_active_state, get_iterable=True)


def get_active(type):
    """Gets all active instances.

    :param type: A supported entity type.
    :type type: class

    :returns: Active entity collection.
    :rtype: list

    """
    return _get_active(type, True)


def get_inactive(type):
    """Gets all inactive instances.

    :param type: A supported entity type.
    :type type: class

    :returns: Inactive entity collection.
    :rtype: list

    """
    return _get_active(type, False)


def get_all(type):
    """Gets all instances of the entity.

    :param type: A supported entity type.
    :type type: class

    :returns: Entity collection.
    :rtype: list

    """
    return get_by_facet(type, order_by=type.ID, get_iterable=True)


def get_by_facet(type, filter=None, order_by=None, get_iterable=False):
    """Gets entity instance by facet.

    :param type: A supported entity type.
    :type type: class

    :param filter: Filter expression.
    :type filter: expression

    :param order_by: Sort expression.
    :type order_by: expression

    :param get_iterable: Flag indicating whether to return an iterable or not.
    :type get_iterable: bool

    :returns: Entity or entity collection.
    :rtype: Sub-class of esdoc_api.lib.repo.models.Entity

    """
    # Defensive programming.
    assert_type(type)

    q = session.query(type)
    if filter is not None:
        q = q.filter(filter)
    if order_by is not None:
        q = q.order_by(order_by)

    return sort(type, q.all()) if get_iterable else q.first()


def get_by_id(type, id):
    """Gets entity instance by id.

    :param type: A supported entity type.
    :type type: class

    :param id: ID of entity.
    :type id: int

    :returns: Entity with matching ID.
    :rtype: Sub-class of esdoc_api.lib.repo.models.Entity

    """
    return get_by_facet(type, filter=type.ID==id)


def get_by_name(type, name):
    """Gets an entity instance by it's name.

    :param type: A supported entity type.
    :type type: class

    :param name: Name of entity.
    :type name: str

    :returns: Entity with matching name.
    :rtype: Sub-class of esdoc_api.lib.repo.models.Entity

    """
    return get_by_facet(type, filter=type.Name==name)


def get_count(type, filter=None):
    """Gets count of entity instances.

    :param type: A supported entity type.
    :type type: class

    :returns: Entity collection count.
    :rtype: int

    """
    # Defensive programming.
    assert_type(type)

    q = session.query(type)
    if filter is not None:
        q = q.filter(filter)

    return q.count()


def insert(instance):
    """Adds a newly created model to the session.

    :param instance: A domain model instance ready for insertion into repository.
    :type instance: Sub-class of esdoc_api.lib.repo.models.Entity

    """
    # Defensive programming.
    assert_instance(instance)
    
    session.insert(instance)


def insert_all(collection):
    """Adds a list of newly created models to the session.

    :param instances: A collection of model instance to be inserted into repo.
    :type instances: iterable

    """
    # Defensive programming.
    assert_collection(collection)

    for instance in collection:
        session.insert(instance)


def delete(instance):
    """Marks entity instance for deletion.

    :param instance: A domain model instance ready for deletion from repository.
    :type item: Sub-class of esdoc_api.lib.repo.models.Entity

    """
    # Defensive programming.
    assert_instance(instance)

    session.delete(instance)


def delete_all(collection):
    """Deletes all entities within collection.

    :param type: A supported entity type.
    :type type: class

    """
    # Defensive programming.
    assert_collection(collection)

    for instance in collection:
        delete(instance)


def delete_all_by_type(type, callback=None):
    """Deletes all entities of passed type.

    :param type: A supported entity type.
    :type type: class

    :param callback: Pointer to a function that will perform callback.
    :type callback: function

    """
    # Defensive programming.
    assert_type(type)

    for instance in get_all(type):
        if callback is not None:
            callback(instance.ID)
        else:
            delete(instance)


def delete_by_facet(type, expression):
    """Delete entity instance by id.

    :param type: A supported entity type.
    :type type: class

    :param facet: Entity facet.
    :type facet: expression

    :param facet: Entity facet value.
    :type facet: object

    """
    # Defensive programming.
    assert_type(type)

    q = session.query(type)
    q = q.filter(expression)
    q.delete()


def delete_by_id(type, id):
    """Delete entity instance by id.

    :param type: A supported entity type.
    :type type: class

    :param id: ID of entity.
    :type id: int

    """
    # Defensive programming.
    assert_type(type)

    delete_by_facet(type, type.ID==id)


def delete_by_name(type, name):
    """Deletes an entity instance by it's name.

    :param type: A supported entity type.
    :type type: class

    :param name: Name of entity.
    :type name: str

    """
    # Defensive programming.
    assert_type(type)
    
    delete_by_facet(type, type.Name==name)


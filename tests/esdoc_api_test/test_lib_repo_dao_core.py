"""
.. module:: esdoc_api_test.test_repo_dao.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: 1st set of repository dao functional tests - N.B. these tests are against a pre-populated repo.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""

# Module imports.
import nose.tools 

import esdoc_api.db.dao as dao
import esdoc_api.db.models as models
import esdoc_api.db.models as models
import esdoc_api.lib.utils.runtime as rt
import esdoc_api_test.utils as tu



def test_assert_type_01():
    # Test valid types assertion.
    for type in models.supported_types:
        models.assert_type(type)
    

@nose.tools.raises(rt.ESDOC_API_Error)
def test_assert_type_02():
    # Test invalid type assertion.
    class TestModelA(object):
        pass
    models.assert_type(TestModelA)


def test_assert_instance_01():
    # Test valid instance assertion.
    for type in models.supported_types:
        models.assert_instance(type())


@nose.tools.raises(rt.ESDOC_API_Error)
def test_assert_instance_02():
    # Test invalid instance assertion.
    class TestModelA(object):
        pass
    models.assert_instance(TestModelA())


def test_assert_iter_01():
    # Test valid collection assertion.
    models.assert_iter(map(lambda st : st(), models.supported_types))


@nose.tools.raises(rt.ESDOC_API_Error)
def test_assert_iter_02():
    # Test invalid collection assertion.
    class TestModelA(object):
        pass
    class TestModelB(object):
        pass
    models.assert_iter([TestModelA(), TestModelB()])


def test_delete_01():
    # Test instance deletion.
    type = models.Project
    instance = tu.get_test_model(type)
    dao.insert(instance)
    count = dao.get_count(type)
    dao.delete(instance)
    tu.assert_int(count - 1, dao.get_count(type))


def test_delete_02():
    # Test collection deletion.
    type = models.IngestEndpoint
    count = dao.get_count(type)
    collection = [
        tu.get_test_model(type),
        tu.get_test_model(type),
        tu.get_test_model(type)
    ]
    dao.insert(collection)
    tu.assert_int(count + len(collection), dao.get_count(type))
    dao.delete(collection)
    tu.assert_int(count, dao.get_count(type))


def test_delete_by_type_01():
    # Test deletion of all instances by type.
    count = dao.get_count(models.IngestURL)
    collection = [
        tu.get_test_model(models.IngestURL),
        tu.get_test_model(models.IngestURL),
        tu.get_test_model(models.IngestURL)
    ]
    dao.insert(collection)
    tu.assert_int(count + len(collection), dao.get_count(models.IngestURL))
    dao.delete_by_type(models.IngestURL)
    tu.assert_int(count, dao.get_count(models.IngestURL))


def test_delete_by_type_02():
    # Test deletion of all instances by type (with deletion callback).
    def delete_callback(id):
        dao.delete_by_id(models.IngestURL, id)
    
    count = dao.get_count(models.IngestURL)
    collection = [
        tu.get_test_model(models.IngestURL),
        tu.get_test_model(models.IngestURL),
        tu.get_test_model(models.IngestURL)
    ]
    dao.insert(collection)
    tu.assert_int(count + len(collection), dao.get_count(models.IngestURL))
    dao.delete_by_type(models.IngestURL, delete_callback)
    tu.assert_int(count, dao.get_count(models.IngestURL))


def test_delete_by_id():
    # Test deletion an instance by type & id.
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    count = dao.get_count(models.Project)
    dao.delete_by_id(models.Project, instance.ID)
    tu.assert_int(count - 1, dao.get_count(models.Project))


def test_delete_by_name():
    # Test deletion an instance by type & name.
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    count = dao.get_count(models.Project)
    dao.delete_by_name(models.Project, instance.Name)
    tu.assert_int(count - 1, dao.get_count(models.Project))


def test_get_active():
    # Test retrieving all active instances of a specified type.
    tu.assert_iter(dao.get_active(models.IngestEndpoint), 8)


def test_get_all():
    # Test retrieving all instances of a specified type.
    tu.assert_iter(dao.get_all(models.DocumentEncoding), 3)


def test_get_by_facet_01():
    # Test retrieving an instance by facet.
    # Insert test instance.
    type = models.DocumentSummary
    instance1 = tu.get_test_model(type)

    # Retrieve instance.
    instance2 = dao.get_by_facet(type, type.ID==instance1.ID)
    tu.assert_object(instance2, type)
    tu.assert_entity(instance1, instance2)


def test_get_by_facet_02():
    # Test retrieving an instance by facet.
    # Insert test instance.
    type = models.DocumentSummary
    instance = tu.get_test_model(type)

    # Retrieve instance via a collection.
    collection = dao.get_by_facet(type, type.ID==instance.ID, get_iterable=True)
    tu.assert_iter(collection, length=1, item_type=type)
    tu.assert_entity(collection[0], instance)


def test_get_by_facet_03():
    # Test retrieving a sorted collection by facet.
    # Insert test collection.
    type = models.DocumentSummary
    dao.delete_by_type(type)
    collection = [
        tu.get_test_model(type),
        tu.get_test_model(type),
        tu.get_test_model(type)
    ]
    dao.insert(collection)

    # Set sort fields.
    fields = sorted(map(lambda i : i.ShortName, collection))

    # Assert sorted collection.
    collection = dao.get_by_facet(type, None, get_iterable=True)
    tu.assert_iter(collection, length=3, item_type=type)
    for i in range(len(collection)):
        tu.assert_str(fields[i], collection[i].ShortName)


def test_get_by_facet_04():
    # Test retrieving an ordered collection by facet.
    # Insert test collection.
    type = models.DocumentSummary
    dao.delete_by_type(type)
    collection = [
        tu.get_test_model(type),
        tu.get_test_model(type),
        tu.get_test_model(type)
    ]
    dao.insert(collection)
    
    # Set sort fields.
    fields = sorted(map(lambda i : i.LongName, collection))
    
    # Assert ordered collection.
    collection = dao.get_by_facet(type, None, get_iterable=True,
                                  order_by=type.LongName)
    tu.assert_iter(collection, length=3, item_type=type)
    for i in range(len(collection)):
        tu.assert_str(fields[i], collection[i].LongName)


def test_get_by_id():
    # Test retrieving an instance by it's id.
    tu.assert_object(dao.get_by_id(models.DocumentEncoding, 1), models.DocumentEncoding)


def test_get_by_name():
    # Test retrieving an instance by it's name.
    tu.assert_object(dao.get_by_name(models.DocumentLanguage, 'Tibetan'), models.DocumentLanguage)


def test_get_count():
    # Test retrieving a count of instances by type.
    tu.assert_int(dao.get_count(models.DocumentEncoding), 3, tu.COMPARE_GTE)


def test_get_inactive():
    # Test retrieving all active instances of a specified type.
    tu.assert_iter(dao.get_inactive(models.IngestEndpoint), 0, length_compare=tu.COMPARE_EXACT)


def test_insert():    
    # Test inserting an instance.
    count = dao.get_count(models.Project)
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    tu.assert_int(count + 1, dao.get_count(models.Project))


def test_insert_all():
    # Test inserting a collection of instances.
    count = dao.get_count(models.IngestEndpoint)
    collection = [
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint)
    ]
    dao.insert(collection)
    tu.assert_int(count + len(collection), dao.get_count(models.IngestEndpoint))

"""
.. module:: esdoc_api_test.test_repo_dao.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://esdocumentation.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: 1st set of repository dao functional tests - N.B. these tests are against a pre-populated repo.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@esdocumentation.org>

"""

# Module imports.
import nose.tools 

import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.models as models
import esdoc_api.lib.repo.models as models
import esdoc_api.lib.utils.runtime as rt
import esdoc_api_test.utils as tu




def test_assert_type_01():
    dao.assert_type(models.Project)
    

@nose.tools.raises(rt.ESDOC_API_Error)
def test_assert_type_02():
    class TestModelA(object):
        pass
    dao.assert_type(TestModelA)


def test_assert_collection_01():
    dao.assert_collection(map(lambda st : st(), models.supported_types))


@nose.tools.raises(rt.ESDOC_API_Error)
def test_assert_collection_02():
    class TestModelA(object):
        pass
    class TestModelB(object):
        pass
    dao.assert_collection([TestModelA(), TestModelB()])


def test_delete():
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    count = dao.get_count(models.Project)
    dao.delete(instance)
    tu.assert_integer(count - 1, dao.get_count(models.Project))


def test_delete_all():
    count = dao.get_count(models.IngestEndpoint)
    collection = [
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint)
    ]
    dao.insert_all(collection)
    tu.assert_integer(count + len(collection), dao.get_count(models.IngestEndpoint))
    dao.delete_all(collection)
    tu.assert_integer(count, dao.get_count(models.IngestEndpoint))


def test_delete_by_id():
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    count = dao.get_count(models.Project)
    dao.delete_by_id(models.Project, instance.ID)
    tu.assert_integer(count - 1, dao.get_count(models.Project))


def test_delete_by_name():
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    count = dao.get_count(models.Project)
    dao.delete_by_name(models.Project, instance.Name)
    tu.assert_integer(count - 1, dao.get_count(models.Project))


def test_get_active():
    tu.assert_collection(dao.get_active(models.IngestEndpoint), 8)


def test_get_all():
    tu.assert_collection(dao.get_all(models.DocumentEncoding), 3)


def test_get_by_id():
    tu.assert_object(dao.get_by_id(models.DocumentEncoding, 1), models.DocumentEncoding)


def test_get_by_name():
    tu.assert_object(dao.get_by_name(models.DocumentLanguage, 'Tibetan'), models.DocumentLanguage)


def test_get_count():
    tu.assert_integer(dao.get_count(models.DocumentEncoding), 3, tu.COMPARE_GTE)


def test_get_inactive():
    tu.assert_collection(dao.get_inactive(models.IngestEndpoint), 0, length_compare=tu.COMPARE_EXACT)


def test_insert():    
    count = dao.get_count(models.Project)
    instance = tu.get_test_model(models.Project)
    dao.insert(instance)
    tu.assert_integer(count + 1, dao.get_count(models.Project))


def test_insert_all():
    count = dao.get_count(models.IngestEndpoint)
    collection = [
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint),
        tu.get_test_model(models.IngestEndpoint)
    ]
    dao.insert_all(collection)
    tu.assert_integer(count + len(collection), dao.get_count(models.IngestEndpoint))

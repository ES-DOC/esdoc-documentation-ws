"""
.. module:: esdoc_api_test.test_models.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Repository models functional tests.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""

# Module imports.
import esdoc_api_test.utils as tu



def test_import_package_01():
    import esdoc_api.db.models as models


def test_import_package_02():
    from esdoc_api.db.models import *


def test_import_model_types():
    import esdoc_api.db.models as models
    assert len(models.supported_types) == 20


def test_conversion():
    import esdoc_api.db.models as models

    target = tu.assert_model_conversion
    for mt in models.supported_types:
        target.description = "testing model conversion :: model = {0}".format(mt)
        yield target, mt


def test_creation():
    import esdoc_api.db.models as models

    target = tu.assert_model_conversion
    for mt in models.supported_types:
        target.description = "testing model creation :: model = {0}".format(mt)
        yield target, mt


def test_persistence():
    import esdoc_api.db.models as models

    target = tu.assert_model_persistence
    for mt in models.supported_types:
        target.description = "testing model persistence :: model = {0}".format(mt)
        yield target, mt


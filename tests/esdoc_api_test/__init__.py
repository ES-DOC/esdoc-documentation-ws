"""
.. module:: esdoc_api_tests.__init__.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://esdocumentation.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Top level package intializer.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@esdocumentation.org>

"""

# Module imports.
import esdoc_api_test.utils as tu
import esdoc_api.lib.utils.runtime as rt



def setup_package():
    rt.log("setting up test runner")
    tu.start_repo_session()


def teardown_package():
    tu.end_repo_session()
    rt.log("tearing down test runner")

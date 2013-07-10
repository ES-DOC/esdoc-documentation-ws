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



def setup_package():
    print "ES-DOC API :: setting up test runner"
    tu.start_repo_session()


def teardown_package():
    tu.end_repo_session()
    print "ES-DOC API :: tearing down test runner"


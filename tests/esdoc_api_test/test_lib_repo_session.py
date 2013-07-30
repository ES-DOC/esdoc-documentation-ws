"""
.. module:: esdoc_api_test.test_repo_session.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://esdocumentation.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Repository session functional tests.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@esdocumentation.org>

"""

# Module imports.
import esdoc_api_test.utils as tu


def test_import():
    import esdoc_api.lib.repo.session as session


def test_is_live():
    import esdoc_api.lib.repo.session as session

    session.assert_is_live()


def test_end():
    import esdoc_api.lib.repo.session as session

    session.end()
    session.assert_is_dead()

    tu.start_repo_session()

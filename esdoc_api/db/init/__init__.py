# -*- coding: utf-8 -*-
"""
.. module:: __init__.py
   :platform: Unix
   :synopsis: Repository initialization entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db.init import initialize_institute
from esdoc_api.db.init import initialize_project
from esdoc_api.utils import runtime as rt



# Repository initializing functions (order matters).
_INITIALIZERS = [
    initialize_institute,
    initialize_project,
]


def execute():
    """Executes repo setup.

    """
    rt.log("DB INITIALIZATION BEGINS")

    for initializer in _INITIALIZERS:
        rt.log("INITIALIZING DB TABLE :: {0}".format(initializer.__name__))
        initializer.execute()

    rt.log("DB INITIALIZATION ENDS")

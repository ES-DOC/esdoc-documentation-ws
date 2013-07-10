"""
.. module:: prodiguer_shared.repo.init.utils.py
   :platform: Unix
   :synopsis: Set of utility data access operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.repo.dao as dao



def set_cache_item(cache, key, type):
    """Assigns an item to the passed cache dictionary.

    """
    if key not in cache:
        cache[key] = dao.get_by_name(type, key)

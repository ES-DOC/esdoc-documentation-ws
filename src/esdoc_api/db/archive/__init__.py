"""
.. module:: __init__.py
   :platform: Unix
   :synopsis: DB document archive operations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from . import (
	write_organized,
	write_pulled
	)



def seed(throttle=0):
	"""Seeds document archive with documents pulled from atom feeds.

    :param int throttle: Limits number of documents to be processed.

	"""
	write_pulled.execute(throttle)


def organize(throttle=0):
	"""Organizes archived documents in readiness for further processing.

    :param int throttle: Limits number of documents to be processed.

	"""
	write_organized.execute(throttle)

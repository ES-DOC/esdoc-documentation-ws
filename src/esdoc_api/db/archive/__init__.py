"""
.. module:: __init__.py
   :platform: Unix
   :synopsis: DB document archive operations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from . import (
	feed_parser,
	uploader
	)



def build(throttle=0):
	"""Builds document archive from documents pulled from atom feeds.

    :param int throttle: Limits number of documents to be pulled.

	"""
	feed_parser.execute(throttle)


def upload(throttle=0):
	"""Uploads document archive to db.

    :param int throttle: Limits number of documents to be uploaded.

	"""
	uploader.execute(throttle)

# -*- coding: utf-8 -*-
"""
.. module:: vocab.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: ES-DOC API db models - vocab domain partition.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from sqlalchemy import Column
from sqlalchemy import Unicode

from esdoc_api.db.models.utils import Entity



# Domain model partition.
_DOMAIN_PARTITION = 'vocab'


class Institute(Entity):
    """Represents an institute with which documents are associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_institute'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    name = Column(Unicode(16), nullable=False, unique=True)
    long_name = Column(Unicode(512), nullable=False)
    country_code = Column(Unicode(2), nullable=False)
    url = Column(Unicode(256))


    @property
    def cache_name(self):
        """Gets instance cache key name.

        """
        return self.name


    @property
    def FullName(self):
        """Gets the full institute name derived by concatanation.

        """
        return self.country_code + u" - " + self.name + u" - " + self.long_name


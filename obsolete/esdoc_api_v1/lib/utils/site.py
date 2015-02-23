# -*- coding: utf-8 -*-

"""
Encapsulates site level meta-info typicallly used in the master page.
"""

# Module imports.
from datetime import datetime

from esdoc_api.lib.utils.site_node import SiteNode
from esdoc_api.lib.utils.site_node import NODE_TYPE_SITE


class Site(SiteNode):
    """
    Encapsulates site level meta information used by the master page during the rendering process.
    """
    def __init__(self, title, version, role='public'):
        """
        Constructor.
        """
        super(Site,self).__init__('frontend', NODE_TYPE_SITE, None)

        # Set default values.
        self.title = title
        self.__version = version
        self.__role = role
        self.href = self.href + '/' + role
        self.__copyright_year = datetime.now().year
        self.__page = None


    @property
    def copyright_year(self):
        """The copyright year displayed in the site page header"""
        return self.__copyright_year


    @property
    def version(self):
        """The site version."""
        return self.__version


    @property
    def page(self):
        """Gets current page being rendered."""
        return self.__page

    @page.setter
    def page(self, value):
        """Sets current page being rendered."""
        self.__page = value


    @property
    def role(self):
        """Gets current user role."""
        return self.__role
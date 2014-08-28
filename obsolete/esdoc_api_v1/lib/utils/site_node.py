"""
Encapsulates a node within the site.
"""

# Module imports.
import string


# Site type declaration.
NODE_TYPE_SITE = 'site'
# Site section type declaration.
NODE_TYPE_SITE_SECTION = 'site-section'
# Page type declaration.
NODE_TYPE_PAGE = 'page'
# Page partition type declaration.
NODE_TYPE_PAGE_PARTITION = 'page-partition'
# Page function type declaration.
NODE_TYPE_PAGE_ACTION = 'page-action'


class SiteNode(object):
    """
    Encapsulates meta-information about a site node such as section, page, function.
    """

    def __init__(self, key, type, parent_node, title=None, short_title=None):
        """
        Constructor.
        """
        # Set default values.
        self.__key = key
        self.__type = type
        self.__href = '/' + key
        if title is not None:
            self.__title = title
        else:
            self.__title = key[0].upper() + key[1:]
        if short_title is not None:
            self._short_title = short_title
        else:
            self._short_title = self.__title
        self.__full_title = self.__title
        self.__is_current = False
        self.__is_live = True
        self.__nodes = []
        self.__parent = parent_node
        self.__roles = ['public', 'internal', 'admin']

        # If parent node defined then set association.
        if parent_node is not None:
            parent_node.nodes.append(self)
            self.__href = parent_node.href + self.__href
            self.__key = parent_node.key + '-' + self.__key
            if parent_node.is_site_section or parent_node.is_page:
                self.__full_title = parent_node.title + ' - ' + self.__title

        self.__icon = self.__key + '.png'
        self.__template = '/pages/' + self.__key + '.xhtml'


    @property
    def key(self):
        """Gets node key (unique at the sibling level)"""
        return self.__key


    @property
    def type(self):
        """Gets node type"""
        return self.__type


    @property
    def parent(self):
        """Gets parent node."""
        return self.__parent


    @property
    def roles(self):
        """Gets set of supported user roles governing access control policy."""
        return self.__roles


    @property
    def href(self):
        """Gets hypertext reference for use in generating anchors.

        """
        return self.__href

    @href.setter
    def href(self, value):
        """Gets hypertext reference for use in generating anchors.

        """
        self.__href = value


    @property
    def title(self):
        """Gets display title"""
        return self.__title

    @title.setter
    def title(self, value):
        """Sets display title"""
        self.__title = value


    @property
    def short_title(self):
        """Gets display short title"""
        return self._short_title

    @short_title.setter
    def short_title(self, value):
        """Sets display short title"""
        self._short_title = value


    @property
    def full__title(self):
        """Gets display full title"""
        return self.__full_title

    @full__title.setter
    def full__title(self, value):
        """Sets display full title"""
        self.__full_title = value


    @property
    def template(self):
        """Gets template used to render page."""
        return self.__template

    @template.setter
    def template(self, value):
        """Sets template used to render page."""
        self.__template = value


    @property
    def icon(self):
        """Gets display icon"""
        return self.__icon

    @icon.setter
    def icon(self, value):
        """Sets display icon"""
        self.__icon = value


    @property
    def is_live(self):
        """Gets a flag indicating whether this node is currently live."""
        return self.__is_live

    @is_live.setter
    def is_live(self, value):
        """Sets a flag indicating whether this node is currently live."""
        self.__is_live = value


    @property
    def is_current(self):
        """Gets a flag indicating whether this node is currently selected."""
        return self.__is_current

    @is_current.setter
    def is_current(self, value):
        """Sets a flag indicating whether this node is currently selected."""
        self.__is_current = value


    @property
    def nodes(self):
        """Gets the collection of associated child nodes."""
        return self.__nodes


    @property
    def is_site(self):
        """Gets flag indicating whether node is a site declaration."""
        return self.__type == NODE_TYPE_SITE


    @property
    def is_site_section(self):
        """Gets flag indicating whether node is a site section declaration."""
        return self.__type == NODE_TYPE_SITE_SECTION


    @property
    def is_page(self):
        """Gets flag indicating whether node is a page declaration."""
        return self.__type == NODE_TYPE_PAGE


    @property
    def is_page_action(self):
        """Gets flag indicating whether node is a page action declaration."""
        return self.__type == NODE_TYPE_PAGE_ACTION


    @property
    def is_page_partition(self):
        """Gets flag indicating whether node is a page partition declaration."""
        return self.__type == NODE_TYPE_PAGE_PARTITION


    def has_access(self, role):
        """
        Returns whether passed role has access to node.
        """
        try:
            return self.__roles.index(role) >= 0
        except ValueError:
            return False


    def full_key(self):
        """
        Returns the full key by contanating the node's key with that of it's parents.
        """
        r = []
        if self.parent is not None:
            r.append(self.parent.key)
            r.append(u'-')
        r.append(self.key)
        return string.join(r, '')


    def append(self, new_node):
        """
        Appends a node to managed collection.
        """
        # Append node with self as parent.
        new_node.parent = self
        self.__nodes.append(new_node)

        # Return node to support chaining.
        return new_node


    def has_permission(self, role):
        """Determines whether role is supported or not.

        """
        return role in self.roles


    def get_pages(self):
        """Returns collection of associated nodes that are pages."""
        for node in self.__nodes:
            if node.is_page == True:
                yield node


    def get_page_partitions(self):
        """Returns collection of associated nodes that are page partitions."""
        for node in self.__nodes:
            if node.is_page_partition == True:
                yield node


    def get_page_actions(self):
        """Returns collection of associated nodes that are page actions."""
        for node in self.__nodes:
            if node.is_page_action == True:
                yield node


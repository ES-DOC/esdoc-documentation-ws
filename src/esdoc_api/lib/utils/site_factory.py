"""
Creates & returns set of node supported across the site.
"""
from esdoc_api.lib.utils.site_node import NODE_TYPE_PAGE_ACTION
import site

# Module imports.
import string
from esdoc_api.lib.utils.site import Site
from esdoc_api.lib.utils.site_node import *


def _create_section_for_about(site):
    s = SiteNode('about', NODE_TYPE_SITE_SECTION, site)
    p = SiteNode('main', NODE_TYPE_PAGE, s, 'about')


def _create_section_for_ingestion(site):
    s = SiteNode('ingestion', NODE_TYPE_SITE_SECTION, site)
    p = SiteNode('main', NODE_TYPE_PAGE, s)


def create_site_map(path, role='public'):
    """Factory method to return a virtual model of the CIM web-site.

    """
    site = Site("ES-DOC API", '0.8.6.3', role)
    
    _create_section_for_about(site)
    _create_section_for_ingestion(site)

    apply_permissions(site)
    set_page(site, path)

    print 'REQUEST :: ROLE = {0}; PATH = {1}; NODE = {2}'.format(role, path, site.page.key)

    return site


def set_page(site, path):
    """Sets page = first page node with matching path.

    """
    for section in site.nodes:
        for page in section.nodes:
            if page.href.startswith(path):
                site.page = page
                section.is_current = True
                return

    for section in site.nodes:
        for page in section.nodes:
            if path.startswith(page.href):
                site.page = page
                section.is_current = True
                return

    # Default node.
    site.page = site.nodes[0].nodes[0]


def apply_permissions(site, nodes=None):
    """Filters node map by role.

    """
    denied = []
    if nodes is None:
        nodes = site.nodes
    for node in nodes:
        if node.has_permission(site.role) == False:
            denied.append(node)
    for node in denied:
        nodes.remove(node)
    for node in nodes:
        apply_permissions(site, node.nodes)
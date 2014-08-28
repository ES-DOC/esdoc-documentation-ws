# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1364915024.1378601
_template_filename='/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src/esdoc_api/templates/pages/site-about.xhtml'
_template_uri='/pages/site-about.xhtml'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace('__anon_0x105999f10', context._clean_inheritance_tokens(), templateuri=u'/master/master.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x105999f10')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/master/master.xhtml', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x105999f10')._populate(_import_ns, [u'*'])
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!--*************************************************-->\n<!-- Page Mako function extensions                   -->\n<!--*************************************************-->\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n<!--*************************************************-->\n<!-- Master template                                 -->\n<!--*************************************************-->\n')
        # SOURCE LINE 9
        __M_writer(u'\n\n\n<!--*************************************************-->\n<!-- Page XHTML Declaration                          -->\n<!--*************************************************-->\n\n<div id="site-home-main-overview-content">\n    <div class="section-header">\n        What is ES-DOC ?\n    </div>\n    <div class="section-content">\n        <p>\n            ES-DOC stands for <b>Earth System - Documentation</b>.  It\'s goal is to provide high quality software tools and services in order to support the distribution of earth science documentation.\n        </p>\n    </div>\n\n    <div class="section-header">\n        What is the CIM ?\n    </div>\n    <div class="section-content">\n        <p>\n            The main objectives of the <a href="http://metafortrac.badc.rl.ac.uk/trac" rel="external">METAFOR</a> project were to develop and promulgate an ipso-facto standard for describing climate models and associated data.\n            This standard has been formalized and named the <b>Common Information Model</b> (CIM).\n            The benefits of adopting a internationally recognized information standard such as the CIM are many:\n        </p>\n        <p style="margin-top: 4px;">\n            <ul>\n                <li>Institutes can share information regarding models, experiments, simulations, data, grids ... etc, in a standardized format;</li>\n                <li>Documentation tools can render CIM compliant information in multiple formats such as html, pdf ...etc;</li>\n                <li>Inter-operability issues can be resolved by adapting existing software to leverage the CIM;</li>\n                <li>Search tools can provide a unified metadata access by ingesting CIM compliant metadata from multiple sources;</li>\n                <li>Differencing engines can attempt to compare climate models.</li>\n            </ul>\n        </p>\n    </div>\n\n\n    <div class="section-header">\n        What is the CIM Eco-System ?\n    </div>\n    <div class="section-content">\n        <p>\n            Built ontop of the CIM standard are a set of community developed tools & web services collectively referred to as the CIM eco-system.\n            Such an eco-system is essential to encouraging adoption of the CIM by the global climate modelling community.\n        </p>\n    </div>\n\n    <div class="section-header">\n        What is the CIM API ?\n    </div>\n    <div class="section-content">\n        <p>\n            The CIM API is a robust set of publicly available web-services.  The API is designed to support an array of use cases such as persistence, search, reporting, & visualisation.  It forms the key infrastructure at the heart of the CIM eco-system.\n        </p>\n    </div>\n\n</div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()



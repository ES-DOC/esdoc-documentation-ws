# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1364915024.21229
_template_filename=u'/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src/esdoc_api/templates/master/master.xhtml'
_template_uri=u'/master/master.xhtml'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['renderSiteMenuItemClass', 'renderPagePartitions', 'renderSiteMenu', 'renderPageActions']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 6
    ns = runtime.TemplateNamespace('__anon_0x10598fd90', context._clean_inheritance_tokens(), templateuri=u'/master/master.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x10598fd90')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x10598fd90')._populate(_import_ns, [u'*'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        def renderSiteMenu():
            return render_renderSiteMenu(context.locals_(__M_locals))
        next = _import_ns.get('next', context.get('next', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n\n<!--*************************************************-->\n<!-- Mako function extensions                        -->\n<!--*************************************************-->\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 20
        __M_writer(u'\n\n')
        # SOURCE LINE 31
        __M_writer(u'\n\n')
        # SOURCE LINE 42
        __M_writer(u'\n\n\n<!--*************************************************-->\n<!-- HTML                                            -->\n<!--*************************************************-->\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n    <!--*************************************************-->\n    <!-- HTML Head                                       -->\n    <!--*************************************************-->\n    <head>\n        <!--*************************************************-->\n        <!-- Standard header declarations                    -->\n        <!--*************************************************-->\n        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n        <title>')
        # SOURCE LINE 57
        __M_writer(escape(c.site.title))
        __M_writer(u' - v')
        __M_writer(escape(c.site.version))
        __M_writer(u'</title>\n        <link rel="shortcut icon" href="/esdoc/img/site-favicon-esdoc.png" type="image/x-icon"/>\n        <!--*************************************************-->\n        <!-- CSS Declaration                                 -->\n        <!--*************************************************-->\n        <!-- Standard -->\n        ')
        # SOURCE LINE 63
        __M_writer(escape(h.stylesheet_link('/esdoc/css/std-html-all.css')))
        __M_writer(u'\n        <!-- JQuery -->\n        ')
        # SOURCE LINE 65
        __M_writer(escape(h.stylesheet_link('/ext/jquery/css/ui/redmond/jquery-ui-1.8.6.custom.css')))
        __M_writer(u'\n        <!-- JQuery - Data-tables-->\n        ')
        # SOURCE LINE 67
        __M_writer(escape(h.stylesheet_link('/ext/jquery/css/datatables/data_table_jui.css')))
        __M_writer(u'\n        <!-- Metafor -->\n        ')
        # SOURCE LINE 69
        __M_writer(escape(h.stylesheet_link('/esdoc/css/mf-site-all.css')))
        __M_writer(u'\n        <!--*************************************************-->\n        <!-- JS Declaration                                  -->\n        <!--*************************************************-->\n        <!-- JQuery -->\n        ')
        # SOURCE LINE 74
        __M_writer(escape(h.javascript_link('/ext/json2.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 75
        __M_writer(escape(h.javascript_link('/ext/underscore-min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 76
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery-1.4.4.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 77
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery-ui-1.8.6.custom.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 78
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.dataTables-1.7.5.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 79
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.validate-.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 80
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.validate.additional-methods.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 81
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.constantfooter.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 82
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.loupe.min.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 83
        __M_writer(escape(h.javascript_link('/ext/jquery/js/jquery.ext.metafor.js')))
        __M_writer(u'\n        <!-- Metafor -->\n        ')
        # SOURCE LINE 85
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/mf-lib.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 86
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/core/mf-lib-core-AjaxHelper.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 87
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/core/mf-lib-core-DataLoader.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 88
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/core/mf-lib-core-Repository.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 89
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/core/mf-lib-core-EntityManager.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 90
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/core/mf-lib-core-SearchEngine.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 91
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/ui/mf-lib-ui-Grid.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 92
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/ui/mf-lib-ui-Utils.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 93
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/ui/mf-lib-ui-Feedback.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 94
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/ui/mf-lib-ui-Toolbar.js')))
        __M_writer(u'\n        ')
        # SOURCE LINE 95
        __M_writer(escape(h.javascript_link('/esdoc/js/lib/ui/mf-lib-ui-Validator.js')))
        __M_writer(u'\n        <script>\n            $(document).ready(function() {\n                $(".mf-site-footer").constantfooter();\n            });\n        </script>\n    </head>\n\n    <!--*************************************************-->\n    <!-- HTML Body                                       -->\n    <!--*************************************************-->\n    <body>\n        <!--*************************************************-->\n        <!-- Site Header                                     -->\n        <!--*************************************************-->\n        <div class="mf-site-header">\n            <div class="inner">\n                <div class="caption">\n                    <span>\n                        <img class="logo"\n                             src="/esdoc/img/site-logo-esdoc.png"\n                             alt="ES-DOC."\n                             title="ES-DOC."\n                             lang="EN" />\n                    </span>\n                    <span class="title">API</span>\n                    <span class="version">v')
        # SOURCE LINE 121
        __M_writer(escape(c.site.version))
        __M_writer(u'</span>\n                </div>\n                <div class="menu">\n                    <div class="primary">\n')
        # SOURCE LINE 125
        __M_writer(escape(renderSiteMenu()))
        __M_writer(u'\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <!--*************************************************-->\n        <!-- Page                                            -->\n        <!--*************************************************-->\n        <div class="mf-page">\n            <div class="inner">\n                <!-- Page Content -->\n                <div class="content">\n')
        # SOURCE LINE 139
        __M_writer(u'                    ')
        __M_writer(escape(next.body()))
        __M_writer(u'\n                </div>\n            </div>\n        </div>\n\n        <!--*************************************************-->\n        <!-- Site Footer                                     -->\n        <!--*************************************************-->\n        <div class="mf-site-footer">\n            <div class="inner">\n                <a href="http://metaforclimate.eu/"\n                   alt="Metafor - European Union"\n                   title="Metafor - European Union"\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-metafor.png"\n                         alt="Metafor - European Union"\n                         title="Metafor - European Union"\n                         lang="EN" />\n                </a>\n                <a href="http://www.earthsystemcurator.org"\n                   alt="Earth System Curator"\n                   title="The Curator project collaboratively develops software infrastructure to support end-to-end modeling in the Earth sciences."\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-esc.gif"\n                         alt="The Curator project collaboratively develops software infrastructure to support end-to-end modeling in the Earth sciences."\n                         title="The Curator project collaboratively develops software infrastructure to support end-to-end modeling in the Earth sciences."\n                         lang="EN" />\n                </a>\n                <a href="http://www.ipsl.fr/"\n                   alt="Institut Pierre Simon Laplace"\n                   title="Institut Pierre Simon Laplace"\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-ipsl.png"\n                         alt="Institut Pierre Simon Laplace"\n                         title="Institut Pierre Simon Laplace"\n                         lang="EN" />\n                </a>\n                <a href="http://badc.nerc.ac.uk"\n                   alt="British Atmospheric Data Centre (BADC)"\n                   title="The British Atmospheric Data Centre (BADC) is the Natural Environment Research Council\'s (NERC) Designated Data Centre for the Atmospheric Sciences."\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-badc.png"\n                         alt="The British Atmospheric Data Centre (BADC) is the Natural Environment Research Council\'s (NERC) Designated Data Centre for the Atmospheric Sciences."\n                         title="The British Atmospheric Data Centre (BADC) is the Natural Environment Research Council\'s (NERC) Designated Data Centre for the Atmospheric Sciences."\n                         lang="EN" />\n                </a>\n                <a href="http://www.dkrz.de/"\n                   alt="Deutsche Klimarechenzentrum (DKRZ)"\n                   title="The German Climate Computing Center is a national facility and a major partner for climate research."\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-dkrz.png"\n                         alt="The German Climate Computing Center is a national facility and a major partner for climate research."\n                         title="The German Climate Computing Center is a national facility and a major partner for climate research."\n                         lang="EN" />\n                </a>\n                <a href="https://is.enes.org/"\n                   alt="IS-ENES"\n                   title="InfraStructure for the European Network for the Earth System Modelling"\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-eu-isenes.png"\n                         alt="InfraStructure for the European Network for the Earth System Modelling "\n                         title="InfraStructure for the European Network for the Earth System Modelling "\n                         lang="EN" />\n                </a>\n                <a href="http://cordis.europa.eu/fp7/home_en.html"\n                   alt="FP7"\n                   title="European Commission"\n                   rel="external">\n                    <img class="logo"\n                         src="/esdoc/img/site-logo-ec.jpg"\n                         alt="FP7"\n                         title="European Commission"\n                         lang="EN" />\n                </a>\n            </div>\n        </div>\n\n        <!--*************************************************-->\n        <!-- Site Widgets                                    -->\n        <!--*************************************************-->\n        <div>\n            <div id="mfSiteProgress">\n                <div class="message ui-state-highlight ui-corner-all"></div>\n            </div>\n            <div id="mfSiteFeedback" class="ui-helper-hidden">\n                <div id="mfSiteFeedbackIcon" class="feedback-icon">Icon to go here</div>\n                <div id="mfSiteFeedbackText" class="feedback-text">Message text to go here</div>\n            </div>\n        </div>\n\n    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_renderSiteMenuItemClass(context,section):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x10598fd90')._populate(_import_ns, [u'*'])
        __M_writer = context.writer()
        # SOURCE LINE 8
        __M_writer(u'\n')
        # SOURCE LINE 9
        if section.is_current == True:
            # SOURCE LINE 10
            __M_writer(u'        current\n')
            pass
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(filters.trim(__M_buf.getvalue()))
    return ''


def render_renderPagePartitions(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x10598fd90')._populate(_import_ns, [u'*'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 22
        __M_writer(u'\n')
        # SOURCE LINE 23
        for page_partition in c.page.get_page_partitions():
            # SOURCE LINE 24
            __M_writer(u'                                    <a id="')
            __M_writer(escape(page_partition.key))
            __M_writer(u'"\n                                       title="')
            # SOURCE LINE 25
            __M_writer(escape(page_partition.title))
            __M_writer(u'"\n                                       class="partition"\n                                       href="#')
            # SOURCE LINE 27
            __M_writer(escape(page_partition.title.lower()))
            __M_writer(u'">\n                                        ')
            # SOURCE LINE 28
            __M_writer(escape(page_partition.title))
            __M_writer(u'\n                                    </a>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_renderSiteMenu(context):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x10598fd90')._populate(_import_ns, [u'*'])
        def renderSiteMenuItemClass(section):
            return render_renderSiteMenuItemClass(context,section)
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 14
        __M_writer(u'\n')
        # SOURCE LINE 15
        for section in c.site.nodes:
            # SOURCE LINE 16
            __M_writer(u'                                        <a title="')
            __M_writer(escape(section.short_title))
            __M_writer(u'"\n                                           href="')
            # SOURCE LINE 17
            __M_writer(escape(section.href))
            __M_writer(u'"\n                                           class="')
            # SOURCE LINE 18
            __M_writer(escape(renderSiteMenuItemClass(section)))
            __M_writer(u'">')
            __M_writer(escape(section.short_title.lower().strip()))
            __M_writer(u'</a>\n')
            pass
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(filters.trim(__M_buf.getvalue()))
    return ''


def render_renderPageActions(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x10598fd90')._populate(_import_ns, [u'*'])
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 33
        __M_writer(u'\n')
        # SOURCE LINE 34
        for page_action in c.page.get_page_actions():
            # SOURCE LINE 35
            __M_writer(u'                                    <button id="')
            __M_writer(escape(page_action.key))
            __M_writer(u'"\n                                            name="')
            # SOURCE LINE 36
            __M_writer(escape(page_action.key))
            __M_writer(u'"\n                                            class="action"\n                                           title="')
            # SOURCE LINE 38
            __M_writer(escape(page_action.title))
            __M_writer(u'"/>\n                                        ')
            # SOURCE LINE 39
            __M_writer(escape(page_action.title))
            __M_writer(u'\n                                    </button>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()



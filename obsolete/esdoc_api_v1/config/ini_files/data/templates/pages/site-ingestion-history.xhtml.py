# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1364915028.371279
_template_filename='/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src/esdoc_api/templates/pages/site-ingestion-history.xhtml'
_template_uri='/pages/site-ingestion-history.xhtml'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['renderIngestCount']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.TemplateNamespace('__anon_0x106aa2250', context._clean_inheritance_tokens(), templateuri=u'/master/master.mako', callables=None, calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x106aa2250')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/master/master.xhtml', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x106aa2250')._populate(_import_ns, [u'*'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        c = _import_ns.get('c', context.get('c', UNDEFINED))
        def renderIngestCount(ingest):
            return render_renderIngestCount(context.locals_(__M_locals),ingest)
        renderDate = _import_ns.get('renderDate', context.get('renderDate', UNDEFINED))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!--*************************************************-->\n<!-- Page Mako function extensions                   -->\n<!--*************************************************-->\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 12
        __M_writer(u'\n\n<!--*************************************************-->\n<!-- Master template                                 -->\n<!--*************************************************-->\n')
        # SOURCE LINE 17
        __M_writer(u'\n\n<!--*************************************************-->\n<!-- Page CSS Declaration                            -->\n<!--*************************************************-->\n\n<!--*************************************************-->\n<!-- Page JS Declaration                             -->\n<!--*************************************************-->\n')
        # SOURCE LINE 26
        __M_writer(escape(h.javascript_link('/js/site/esdoc-site-ingestion-history.js')))
        __M_writer(u'\n\n<!--*************************************************-->\n<!-- Page XHTML Declaration                          -->\n<!--*************************************************-->\n<!-- Ingest History -->\n<div class="ui-corner-all">\n    <table cellpadding="0" cellspacing="0" border="0"  style="width: 100%;" class="mf-datatable">\n        <thead>\n            <tr>\n                <!-- Data Columns -->\n                <th title="Institute">Institute</th>\n                <th title="Ingest Source">Source</th>\n                <th title="Ingest Feed URL">Feed URL</th>\n                <th title="Ingest Date">Date</th>\n                <th title="Ingest Count">Count</th>\n                <th title="Ingest Status">Status</th>\n            </tr>\n        </thead>\n        <tbody>\n')
        # SOURCE LINE 46
        for item in c.ingest_history:
            # SOURCE LINE 47
            __M_writer(u'            <tr class="')
            __M_writer(escape(item.State.Name))
            __M_writer(u'">\n                <!-- Data Columns -->\n                <td class="center">')
            # SOURCE LINE 49
            __M_writer(escape(item.Endpoint.Institute.Name))
            __M_writer(u'</td>\n                <td class="center">')
            # SOURCE LINE 50
            __M_writer(escape(item.Endpoint.MetadataSource))
            __M_writer(u'</td>\n                <td class="center">')
            # SOURCE LINE 51
            __M_writer(escape(item.Endpoint.IngestURL))
            __M_writer(u'</td>\n                <td class="center">')
            # SOURCE LINE 52
            __M_writer(escape(renderDate(item.StartDateTime)))
            __M_writer(u'</td>\n                <td class="center">')
            # SOURCE LINE 53
            __M_writer(escape(renderIngestCount(item)))
            __M_writer(u'</td>\n                <td class="center">')
            # SOURCE LINE 54
            __M_writer(escape(item.State.Name))
            __M_writer(u'</td>\n            </tr>\n')
            pass
        # SOURCE LINE 57
        __M_writer(u'        </tbody>\n    </table>\n</div><!--end Ingest History -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_renderIngestCount(context,ingest):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x106aa2250')._populate(_import_ns, [u'*'])
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n')
        # SOURCE LINE 7
        if ingest.State.Name == 'RUNNING':
            # SOURCE LINE 8
            __M_writer(u'        --\n')
            # SOURCE LINE 9
        else:
            # SOURCE LINE 10
            __M_writer(u'        ')
            __M_writer(escape(ingest.Count))
            __M_writer(u'\n')
            pass
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(filters.trim(__M_buf.getvalue()))
    return ''



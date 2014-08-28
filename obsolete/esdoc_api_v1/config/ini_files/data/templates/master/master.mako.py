# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1364915024.1910341
_template_filename=u'/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src/esdoc_api/templates/master/master.mako'
_template_uri=u'/master/master.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['renderDate', 'renderField']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.ModuleNamespace(u'strftime', context._clean_inheritance_tokens(), callables=None, calling_uri=_template_uri, module=u'time')
    context.namespaces[(__name__, u'strftime')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!--*************************************************-->\n<!-- Mako function extensions                        -->\n<!--*************************************************-->\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 18
        __M_writer(u'\n\n')
        # SOURCE LINE 32
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_renderDate(context,datetime,none_text=None,format=True):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n')
        # SOURCE LINE 7
        if datetime is not None:
            # SOURCE LINE 8
            if format == True:
                # SOURCE LINE 9
                __M_writer(u'            ')
                __M_writer(escape(datetime.strftime("%Y--%m--%d")))
                __M_writer(u'\n')
                # SOURCE LINE 10
            else:
                # SOURCE LINE 11
                __M_writer(u'            ')
                __M_writer(escape(datetime.date()))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 13
        elif none_text is not None:
            # SOURCE LINE 14
            __M_writer(u'        ')
            __M_writer(escape(none_text))
            __M_writer(u'\n')
            # SOURCE LINE 15
        else:
            # SOURCE LINE 16
            __M_writer(u'        "--"\n')
            pass
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(filters.trim(__M_buf.getvalue()))
    return ''


def render_renderField(context,field,none_text=None,index=0):
    context.caller_stack._push_frame()
    try:
        context._push_buffer()
        __M_writer = context.writer()
        # SOURCE LINE 20
        __M_writer(u'\n')
        # SOURCE LINE 21
        if field is not None and field != 'None':
            # SOURCE LINE 22
            if index > 0:
                # SOURCE LINE 23
                __M_writer(u'            ')
                __M_writer(escape(field[:index]))
                __M_writer(u'\n')
                # SOURCE LINE 24
            else:
                # SOURCE LINE 25
                __M_writer(u'            ')
                __M_writer(escape(field))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 27
        elif none_text is not None:
            # SOURCE LINE 28
            __M_writer(u'        ')
            __M_writer(escape(none_text))
            __M_writer(u'\n')
            # SOURCE LINE 29
        else:
            # SOURCE LINE 30
            __M_writer(u'        --\n')
            pass
    finally:
        __M_buf, __M_writer = context._pop_buffer_and_writer()
        context.caller_stack._pop_frame()
    __M_writer(filters.trim(__M_buf.getvalue()))
    return ''



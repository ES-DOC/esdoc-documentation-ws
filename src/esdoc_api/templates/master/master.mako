<!--*************************************************-->
<!-- Mako function extensions                        -->
<!--*************************************************-->
<%namespace name="strftime" module="time"/>

<%def name="renderDate(datetime, none_text = None, format=True)" filter="trim">
    % if datetime is not None:
        % if format == True:
            ${datetime.strftime("%Y--%m--%d")}
        % else:
            ${datetime.date()}
        % endif
    % elif none_text is not None:
        ${none_text}
    % else:
        "--"
    % endif
</%def>

<%def name="renderField(field, none_text=None, index=0)" filter="trim">
    % if field is not None and field != 'None':
        % if index > 0:
            ${field[:index]}
        % else:
            ${field}
        % endif
    % elif none_text is not None:
        ${none_text}
    % else:
        --
    % endif
</%def>

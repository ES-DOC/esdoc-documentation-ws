"""Set of string utilitiy functions

"""
# Module imports.


# Module exports.
__all__ = ['convert_to_camel_case', 'convert_to_pascal_case']


def convert_to_camel_case(name, separator='_'):
    """Converts passed name to camel case.

    Keyword Arguments:
    name - a name as specified in onology spec.
    separator - separator to use in order to split name into constituent parts.

    """
    r = ''
    if name is not None:
        s = name.split(separator)
        for s in s:
            if (len(s) > 0):
                r += s[0].upper()
                if (len(s) > 1):
                    r += s[1:]
    return r


def convert_to_pascal_case(name, separator='_'):
    """Converts passed name to camel case.

    Keyword Arguments:
    name - a name as specified in onology spec.
    separator - separator to use in order to split name into constituent parts.

    """
    r = ''
    s = convert_to_camel_case(name, separator)
    if (len(s) > 0):
        r += s[0].lower()
        if (len(s) > 1):
            r += s[1:]
    return r
"""
.. module:: esdoc_api.lib.utils.convertors.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of conversion utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import re
import types


    
def convert_dict_keys(d, key_formatter):
    """Converts keys of a dictionary using the passed key formatter.

    :param d: A dictionary.
    :type d: dict

    :param key_formatter: A dictionary key formatter function pointer.
    :type key_formatter: function

    :returns: A dictionary with it's keys formatted accordingly.
    :rtype: dict

    """
    # Escape if not passed a dictionary.
    if isinstance(d, dict) == False:
        return d

    r = {}

    for key, item in d.items():
        value = None

        # .. sub-dictionaries.
        if isinstance(item, dict):
            value = convert_dict_keys(item, key_formatter)

        # .. collections.
        elif isinstance(item, types.ListType):
            value = []
            for sub_item in item:
                value.append(convert_dict_keys(sub_item, key_formatter))

        # .. primitives.
        else:
            value = item

        r[key_formatter(key)] = value

    return r


def convert_to_camel_case(target, separator='_'):
    """Converts passed name to camel case.

    :param target: A string to be converted.
    :type target: str

    :param separator: A separator used to split target string into constituent parts.
    :type separator: str

    :returns: The target string converted to camel case.
    :rtype: str
    
    """
    # Default conversions.
    if target in ['id']:
        return target.upper()

    r = ''
    if target is not None:
        s = target.split(separator)
        for s in s:
            if (len(s) > 0):
                r += s[0].upper()
                if (len(s) > 1):
                    r += s[1:]
    return r


def convert_to_pascal_case(target, separator='_'):
    """Converts passed name to pascal case, e.g. FullAddress > fullAddress.

    :param target: A string to be converted.
    :type target: str

    :param separator: A separator used to split target string into constituent parts.
    :type separator: str

    :returns: The target string converted to pascal case.
    :rtype: str

    """
    # Default conversions.
    if target in ['ID']:
        return target.lower()

    r = ''
    s = convert_to_camel_case(target, separator)
    if (len(s) > 0):
        r += s[0].lower()
        if (len(s) > 1):
            r += s[1:]
    return r


def convert_to_spaced_case(value):
    """Helper function to convert a string value from camel case to spaced case.

    :param value: A string for conversion.
    :type value: str

    :returns: A string converted to spaced case.
    :rtype: str

    """
    if value.find(" ") == -1:
        return re.sub("([A-Z])"," \g<0>", value).strip()
    else:
        return value



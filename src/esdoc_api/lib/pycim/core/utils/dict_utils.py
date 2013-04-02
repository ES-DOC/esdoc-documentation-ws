"""Set of dictionary utilitiy functions

"""
# Module imports.
import types

# Module exports.
__all__ = ['convert_dict_keys']


def convert_dict_keys(d, key_formatter):
    """
    Converts keys of a dictionary using the passed key formatter.

    Keyword Arguments:
    d - a dictionary to be converted.
    key_formatter - a dictionary key formatting function pointer.

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

"""
.. module:: esdoc_api.lib.utils.string.py
   :copyright: Copyright "May 13, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of string related utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import re



def _replace_protected_chars(keyword):
    """
    Replaces protected characters in the keyword.
    """
    k = keyword.replace('%', '::')
    return k


def _format_keyword(keyword, strip_chars = []):
    """Returns formatted keywords.

    """
    k = keyword.upper()

    # Strip characters.
    if strip_chars is not None:
        for sc in strip_chars:
            k = k.replace(sc.upper(), u'')
        k = k.strip()

    # Assign.
    if len(k) > 0:
        k = '<' + _replace_protected_chars(k) + '>'

    return k


def get_keywords(target, strip_chars = [], split_char=None):
    # Defensive programming.
    if target is None:
        raise UnboundLocalError('target')

    r = ''

    k = str(target)
    if k is not None and len(k) > 0:
        k = k.strip().upper()
        if split_char is not None:
            for k in sorted(set(k.split(split_char)), key=len, reverse=True):
                r += _format_keyword(k, strip_chars)
        else:
            r += _format_keyword(k, strip_chars)

    return r


def get_rows(text, split='|'):
    """Parses incoming data and yields each row as an array of values.

    """
    for row in [l.split(split) for l in text.splitlines()]:
        for i in range(len(row)):
            row[i] = row[i].strip()
        yield row



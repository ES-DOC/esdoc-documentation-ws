"""
.. module:: esdoc_api.lib.pyesdoc.serialization.__init__.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package initialisor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from collections import namedtuple

from esdoc_api.lib.pyesdoc.utils.ontologies import is_supported as is_supported_ontology
from esdoc_api.lib.pyesdoc.serialization.decoder_json import decode as json_decoder
from esdoc_api.lib.pyesdoc.serialization.decoder_xml import decode as xml_decoder
from esdoc_api.lib.pyesdoc.serialization.encoder_json import encode as json_encoder
from esdoc_api.lib.pyesdoc.serialization.encoder_xml import encode as xml_encoder
from esdoc_api.lib.pyesdoc.utils.exception import PYESDOC_Exception



class _ContextInfo(object):
    """Contextual information passed around during serialization operations.

    """
    def __init__(self,
                 ontology_name,
                 ontology_version,
                 encoding,
                 type=None,
                 representation=None,
                 instance=None):
        self.ontology_name = str(ontology_name).lower()
        self.ontology_version = str(ontology_version).upper()
        self.encoding = str(encoding).lower()
        self.type = type
        self.representation = representation
        self.instance = instance


# Set of supported ESDOC encodings.
ESDOC_ENCODING_JSON = 'json'
ESDOC_ENCODING_XML = 'xml'

# Set of decoders.
_decoders = {
    ESDOC_ENCODING_JSON : json_decoder,
    ESDOC_ENCODING_XML : xml_decoder,
}

# Set of encoders.
_encoders = {
    ESDOC_ENCODING_JSON : json_encoder,
    ESDOC_ENCODING_XML : xml_encoder,
}



def decode(representation, ontology_name, ontology_version, encoding):
    """Decodes a esdoc_api.lib.pyesdoc document representation.

    :param representation: A document representation (e.g. utf-8).
    :type representation: str

    :param ontology_name: Name of ontology from which representation is derived (e.g. CIM).
    :type ontology_name: str

    :param ontology_version: Version of ontology from which representation is derived (e.g. v1).
    :type ontology_version: str

    :param encoding: A document encoding (e.g. json).
    :type encoding: str

    :returns: A esdoc_api.lib.pyesdoc document instance.
    :rtype: object

    """
    # Defensive programming.
    if representation is None:
        raise PYESDOC_Exception('Document instances cannot be decoded from null objects.')
    if not is_supported_ontology(ontology_name, ontology_version):
        msg = "Ontology {0} v{1} is unsupported."
        raise PYESDOC_Exception(msg.format(ontology_name, ontology_version))
    if not encoding in _decoders:
        raise PYESDOC_Exception("{0} decoding unsupported.".format(encoding))

    ctx = _ContextInfo(ontology_name, ontology_version, encoding, representation=representation)
    _decoders[encoding](ctx)

    return ctx.instance


def encode(instance, ontology_name, ontology_version, encoding):
    """Encodes a esdoc_api.lib.pyesdoc document instance.

    :param instance: esdoc_api.lib.pyesdoc document instance.
    :type instance: object

    :param ontology_name: Name of ontology from which representation is derived (e.g. CIM).
    :type ontology_name: str

    :param ontology_version: Version of ontology from which representation is derived (e.g. v1).
    :type ontology_version: str
    
    :param encoding: A document encoding (e.g. json).
    :type encoding: str

    :returns: A esdoc_api.lib.pyesdoc document instance.
    :rtype: object

    """
    # Defensive programming.
    if instance is None:
        raise PYESDOC_Exception('Cannot encode null objects.')
    if not is_supported_ontology(ontology_name, ontology_version):
        msg = "Schema {0} v{1} (encoding {2}) is unsupported."
        raise PYESDOC_Exception(msg.format(ontology_name, ontology_version, encoding))
    if not encoding in _encoders:
        raise PYESDOC_Exception("{0} encoding unsupported.".format(encoding))

    ctx = _ContextInfo(ontology_name, ontology_version, encoding, instance=instance)
    _encoders[encoding](ctx)

    return ctx.representation
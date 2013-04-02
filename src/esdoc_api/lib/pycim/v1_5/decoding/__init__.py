"""A set of cim 1.5 decoding packages.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.427917.
"""

# Module imports.
from lxml import etree as et

from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import get_cim_xml
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import decode_xml
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_activity_package import decode_ensemble
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_activity_package import decode_numerical_experiment
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_activity_package import decode_simulation_composite
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_activity_package import decode_simulation_run
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_data_package import decode_data_object
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_grids_package import decode_grid_spec
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_quality_package import decode_cim_quality
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_shared_package import decode_platform
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_software_package import decode_model_component
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_software_package import decode_processor_component

# Module exports.
__all__ = ['decode_ensemble', 'decode_numerical_experiment', 'decode_simulation_composite', 'decode_simulation_run', 'decode_data_object', 'decode_grid_spec', 'decode_cim_quality', 'decode_platform', 'decode_model_component', 'decode_processor_component']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="2013-01-30 15:45:18.427917"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"


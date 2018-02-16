# -*- coding: utf-8 -*-
#                   .___
#   ____   ______ __| _/____   ____           __  _  ________
# _/ __ \ /  ___// __ |/  _ \_/ ___\   ______ \ \/ \/ /  ___/
# \  ___/ \___ \/ /_/ (  <_> )  \___  /_____/  \     /\___ \
#  \___  >____  >____ |\____/ \___  >           \/\_//____  >
#      \/     \/     \/           \/                      \/
#
"""
.. module:: esdoc_api.__init__.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Package initializer.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
__title__ = 'es-doc web service'
__version__ = '0.10.0.0.0'
__author__ = 'ES-DOC'
__license__ = 'GPL'
__copyright__ = 'Copyright 2018: IPSL'

from esdoc_api.app import run, stop
from esdoc_api.utils.config import data as config

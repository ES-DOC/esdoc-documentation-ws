# -*- coding: utf-8 -*-
#                             __
#   _______________________ _/  |______            __  _  ________
# _/ __ \_  __ \_  __ \__  \\   __\__  \    ______ \ \/ \/ /  ___/
# \  ___/|  | \/|  | \// __ \|  |  / __ \_ /_____/  \     /\___ \
#  \___  >__|   |__|  (____  /__| (____  /           \/\_//____  >
#      \/                  \/          \/                      \/
#
"""
.. module:: esdoc_api.__init__.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Package initializer.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
__title__ = 'es-doc web service'
__version__ = '0.9.5.3.0'
__author__ = 'ES-DOC'
__license__ = 'GPL'
__copyright__ = 'Copyright 2016: IPSL'

from esdoc_api.app import run, stop
from esdoc_api.utils.config import data as config

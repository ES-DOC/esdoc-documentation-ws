# -*- coding: utf-8 -*-
"""
.. module:: initialize_project.py
   :platform: Unix
   :synopsis: Initializes collection of supported projects.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models, session



def execute():
    """Initializes collection of supported projects.

    """
    # Global.
    i = models.Project()
    i.name = u"global"
    i.description = u"An application placeholder that acts as a null reference"
    session.insert(i)

    # Test.
    i = models.Project()
    i.name = u"Test"
    i.description = u"A test project plceholder"
    session.insert(i)

    # CMIP5.
    i = models.Project()
    i.name = u"CMIP5"
    i.description = u"Coupled Model Intercomparison Project Phase 5"
    i.url = u"http://cmip-pcmdi.llnl.gov/cmip5/"
    session.insert(i)

    # DCMIP-2012
    i = models.Project()
    i.name = u"DCMIP-2012"
    i.description = u"2012 Dynamical Core Model Intercomparison Project"
    i.url = u"http://earthsystemcog.org/projects/dcmip-2012/"
    session.insert(i)

    # QED-2013
    i = models.Project()
    i.name = u"QED-2013"
    i.description = u"2013 Statistical Downscaling Dynamical Core Model Intercomparison Project"
    i.url = u"http://earthsystemcog.org/projects/downscaling-2013/"
    session.insert(i)

    # ESPS
    i = models.Project()
    i.name = u"ESPS"
    i.description = u"Earth System Prediction Suite"
    i.url = u"https://www.earthsystemcog.org/projects/esps/"
    session.insert(i)

    # DOWNSCALING
    i = models.Project()
    i.name = u"DOWNSCALING-METADATA"
    i.description = u"Downscaling Metadata"
    i.url = u"https://www.earthsystemcog.org/projects/downscalingmetadata/"
    session.insert(i)

    # ES-FDL
    i = models.Project()
    i.name = u"ES-FDL"
    i.description = u"Earth System Framework Description Lanaguage"
    i.url = u"https://earthsystemcog.org/projects/es-fdl"
    session.insert(i)

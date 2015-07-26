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
    i.Name = u"global"
    i.Description = u"An application placeholder that acts as a null reference"
    session.insert(i)

    # Test.
    i = models.Project()
    i.Name = u"Test"
    i.Description = u"A test project plceholder"
    session.insert(i)

    # CMIP5.
    i = models.Project()
    i.Name = u"CMIP5"
    i.Description = u"Coupled Model Intercomparison Project Phase 5"
    i.URL = u"http://cmip-pcmdi.llnl.gov/cmip5/"
    session.insert(i)

    # DCMIP-2012
    i = models.Project()
    i.Name = u"DCMIP-2012"
    i.Description = u"2012 Dynamical Core Model Intercomparison Project"
    i.URL = u"http://earthsystemcog.org/projects/dcmip-2012/"
    session.insert(i)

    # QED-2013
    i = models.Project()
    i.Name = u"QED-2013"
    i.Description = u"2013 Statistical Downscaling Dynamical Core Model Intercomparison Project"
    i.URL = u"http://earthsystemcog.org/projects/downscaling-2013/"
    session.insert(i)

    # ESPS
    i = models.Project()
    i.Name = u"ESPS"
    i.Description = u"Earth System Prediction Suite"
    i.URL = u"https://www.earthsystemcog.org/projects/esps/"
    session.insert(i)

    # DOWNSCALING
    i = models.Project()
    i.Name = u"DOWNSCALING-METADATA"
    i.Description = u"Downscaling Metadata"
    i.URL = u"https://www.earthsystemcog.org/projects/downscalingmetadata/"
    session.insert(i)

    # ES-FDL
    i = models.Project()
    i.Name = u"ES-FDL"
    i.Description = u"Earth System Framework Description Lanaguage"
    i.URL = u"https://earthsystemcog.org/projects/es-fdl"
    session.insert(i)

"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.project import Project

# Module exports.
__all__ = ['populate_project']



def populate_project():
    """Populates collection of supported projects.

    Keyword Arguments:
    session - db sesssion.
    
    """
    # CMIP5.
    p = Project()
    p.Name = "CMIP5"
    p.Description = "Coupled Model Intercomparison Project Phase 5"
    p.URL = "http://cmip-pcmdi.llnl.gov/cmip5/"

    # DCMIP-2012
    p = Project()
    p.Name = "DCMIP-2012"
    p.Description = "2012 Dynamical Core Model Intercomparison Project"
    p.URL = "http://earthsystemcog.org/projects/dcmip-2012/"

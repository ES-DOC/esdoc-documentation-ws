"""Populates collection of supported ingest endpoints.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import datetime

from esdoc_api.models.entities.ingest_endpoint import IngestEndpoint
from esdoc_api.models.entities.institute import Institute

# Module exports.
__all__ = ['populate_ingest_endpoint']


def populate_ingest_endpoint():
    """Populates collection of supported ingest endpoints.

    Keyword Arguments:
    session - db sesssion.
    """
    # CIMP5 Questionnaire - Models.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - CIMP5 Questionnaire - Models"
    ep.IngestorType = 'cmip5q'
    ep.ContactName =  "Gerard Devine"
    ep.ContactEmail =  "g.m.devine@reading.ac.uk"
    ep.ContactTelephone =  "+44 (0)118 378 6021"
    ep.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/component/"
    ep.Institute = Institute.get_by_name("BADC")
    ep.MetadataSource = 'Metafor Questionnaire'
    ep.Priority = 10000

    # CIMP5 Questionnaire - Experiments.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - CIMP5 Questionnaire - Experiments"
    ep.IngestorType = 'cmip5q'
    ep.ContactName =  "Gerard Devine"
    ep.ContactEmail =  "g.m.devine@reading.ac.uk"
    ep.ContactTelephone =  "+44 (0)118 378 6021"
    ep.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/experiment/"
    ep.Institute = Institute.get_by_name("BADC")
    ep.MetadataSource = 'Metafor Questionnaire'
    ep.Priority = 10000

    # CIMP5 Questionnaire - Platforms.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - CIMP5 Questionnaire - Platforms"
    ep.IngestorType = 'cmip5q'
    ep.ContactName =  "Gerard Devine"
    ep.ContactEmail =  "g.m.devine@reading.ac.uk"
    ep.ContactTelephone =  "+44 (0)118 378 6021"
    ep.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/platform/"
    ep.Institute = Institute.get_by_name("BADC")
    ep.MetadataSource = 'Metafor Questionnaire'
    ep.Priority = 10000

    # CIMP5 Questionnaire - All.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - CIMP5 Questionnaire"
    ep.IngestorType = 'cmip5q'
    ep.ContactName =  "Gerard Devine"
    ep.ContactEmail =  "g.m.devine@reading.ac.uk"
    ep.ContactTelephone =  "+44 (0)118 378 6021"
    ep.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/all"
    ep.Institute = Institute.get_by_name("BADC")
    ep.MetadataSource = 'Metafor Questionnaire'
    ep.Priority = 1000

    # CIM QC Tool.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - CIMP5 Quality Control"
    ep.IngestorType = 'cmip5qc'
    ep.ContactName =  "Martina Stockhause"
    ep.ContactEmail =  "stockhause@dkrz.de"
    ep.ContactTelephone =  "+49 (0)40-460094-122"
    ep.IngestURL =  "http://cera-www.dkrz.de/WDCC/CMIP5/feed"
    ep.Institute = Institute.get_by_name("MPI-M")
    ep.MetadataSource = 'DKRZ CERA database'
    ep.Priority = 100

    # DCMIP-2012 - file system feed.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - DCMIP-2012"
    ep.IngestorType = 'dcmip2012'
    ep.ContactName =  "Allyn Treshanksky"
    ep.ContactEmail =  "allyn.treshansky@noaa.gov"
    ep.ContactTelephone =  "+1 303-497-7734"
    ep.IngestURL =  "http://hydra.fsl.noaa.gov/cim-atom-feed/feeds/cim"
    ep.Institute = Institute.get_by_name("NOAA-GFDL")
    ep.MetadataSource = 'ES-DOC django-cim-forms'
    ep.Priority = 10000
    
    # DCMIP-2012 - dynamic feed.
    ep = IngestEndpoint()
    ep.IsActive = True
    ep.Description = "ATOM - DCMIP-2012"
    ep.IngestorType = 'dcmip2012'
    ep.ContactName =  "Allyn Treshanksky"
    ep.ContactEmail =  "allyn.treshansky@noaa.gov"
    ep.ContactTelephone =  "+1 303-497-7734"
    ep.IngestURL =  "http://earthsystemcog.org/metadata/feed/dycore/"
    ep.Institute = Institute.get_by_name("NOAA-GFDL")
    ep.MetadataSource = 'ES-DOC django-cim-forms'
    ep.Priority = 10000


"""
.. module:: esdoc_api.lib.repo.init.populate_ingest_endpoint.py
   :platform: Unix
   :synopsis: Populates collection of supported ingestion endpoints.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session



def populate_ingest_endpoint():
    """Populates collection of supported ingest endpoints.

    Keyword Arguments:
    session - db sesssion.
    """
    # CIMP5 Questionnaire - Models.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - CIMP5 Questionnaire - Models"
    i.IngestorType = 'cmip5q'
    i.ContactName =  "Gerard Devine"
    i.ContactEmail =  "g.m.devine@reading.ac.uk"
    i.ContactTelephone =  "+44 (0)118 378 6021"
    i.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/component/"
    i.Institute_ID = dao.get_by_name(models.Institute, "BADC").ID
    i.MetadataSource = 'Metafor Questionnaire'
    i.Priority = 10000
    session.insert(i)

    # CIMP5 Questionnaire - Experiments.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - CIMP5 Questionnaire - Experiments"
    i.IngestorType = 'cmip5q'
    i.ContactName =  "Gerard Devine"
    i.ContactEmail =  "g.m.devine@reading.ac.uk"
    i.ContactTelephone =  "+44 (0)118 378 6021"
    i.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/experiment/"
    i.Institute_ID = dao.get_by_name(models.Institute, "BADC").ID
    i.MetadataSource = 'Metafor Questionnaire'
    i.Priority = 10000
    session.insert(i)

    # CIMP5 Questionnaire - Platforms.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - CIMP5 Questionnaire - Platforms"
    i.IngestorType = 'cmip5q'
    i.ContactName =  "Gerard Devine"
    i.ContactEmail =  "g.m.devine@reading.ac.uk"
    i.ContactTelephone =  "+44 (0)118 378 6021"
    i.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/platform/"
    i.Institute_ID = dao.get_by_name(models.Institute, "BADC").ID
    i.MetadataSource = 'Metafor Questionnaire'
    i.Priority = 10000
    session.insert(i)

    # CIMP5 Questionnaire - All.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - CIMP5 Questionnaire"
    i.IngestorType = 'cmip5q'
    i.ContactName =  "Gerard Devine"
    i.ContactEmail =  "g.m.devine@reading.ac.uk"
    i.ContactTelephone =  "+44 (0)118 378 6021"
    i.IngestURL =  "http://q.cmip5.ceda.ac.uk/feeds/cmip5/all"
    i.Institute_ID = dao.get_by_name(models.Institute, "BADC").ID
    i.MetadataSource = 'Metafor Questionnaire'
    i.Priority = 1000
    session.insert(i)

    # CIM QC Tool.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - CIMP5 Quality Control"
    i.IngestorType = 'cmip5qc'
    i.ContactName =  "Martina Stockhause"
    i.ContactEmail =  "stockhause@dkrz.de"
    i.ContactTelephone =  "+49 (0)40-460094-122"
    i.IngestURL =  "http://cera-www.dkrz.de/WDCC/CMIP5/feed"
    i.Institute_ID = dao.get_by_name(models.Institute, "MPI-M").ID
    i.MetadataSource = 'DKRZ CERA database'
    i.Priority = 100
    session.insert(i)

    # DCMIP-2012 - file system feed.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - DCMIP-2012"
    i.IngestorType = 'dcmip2012'
    i.ContactName =  "Allyn Treshanksky"
    i.ContactEmail =  "allyn.treshansky@noaa.gov"
    i.ContactTelephone =  "+1 303-497-7734"
    i.IngestURL =  "http://hydra.fsl.noaa.gov/cim-atom-feed/feeds/cim"
    i.Institute_ID = dao.get_by_name(models.Institute, "NOAA-GFDL").ID
    i.MetadataSource = 'ES-DOC django-cim-forms'
    i.Priority = 10000
    session.insert(i)
    
    # DCMIP-2012 - dynamic feed.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - DCMIP-2012"
    i.IngestorType = 'dcmip2012'
    i.ContactName =  "Allyn Treshanksky"
    i.ContactEmail =  "allyn.treshansky@noaa.gov"
    i.ContactTelephone =  "+1 303-497-7734"
    i.IngestURL =  "http://earthsystemcog.org/metadata/feed/dycore/"
    i.Institute_ID = dao.get_by_name(models.Institute, "NOAA-GFDL").ID
    i.MetadataSource = 'ES-DOC django-cim-forms'
    i.Priority = 10000
    session.insert(i)

    # QED-2013 - dynamic feed.
    i = models.IngestEndpoint()
    i.IsActive = True
    i.Description = "ATOM - QED-2013"
    i.IngestorType = 'qed2013'
    i.ContactName =  "Allyn Treshanksky"
    i.ContactEmail =  "allyn.treshansky@noaa.gov"
    i.ContactTelephone =  "+1 303-497-7734"
    i.IngestURL =  "http://earthsystemcog.org/dcf/feed/downscaling/"
    i.Institute_ID = dao.get_by_name(models.Institute, "NOAA-GFDL").ID
    i.MetadataSource = 'ES-DOC django-cim-forms'
    i.Priority = 10000
    session.insert(i)


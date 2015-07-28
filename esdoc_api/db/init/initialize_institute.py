# -*- coding: utf-8 -*-
"""
.. module:: initialize_institute.py
   :platform: Unix
   :synopsis: Initializes collection of supported institutes.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models, session



def execute():
    """Initializes collection of supported institutes.

    """
    # Undefined.
    i = models.Institute()
    i.Name = u"--"
    i.LongName = u"Placeholder for scenario when an institute is undefined"
    i.CountryCode = u"--"
    session.insert(i)

    # Test.
    i = models.Institute()
    i.Name = u"TEST"
    i.LongName = u"Placeholder for test scenrarios"
    i.CountryCode = u"--"
    session.insert(i)

    # BADC.
    i = models.Institute()
    i.Name = u"BADC"
    i.LongName = u"British Atmospheric Data Centre"
    i.CountryCode = u"UK"
    i.URL = u"http://badc.nerc.ac.uk/home/index.html"
    session.insert(i)

    # COLA-CFS.
    i = models.Institute()
    i.Name = u"COLA-CFS"
    i.LongName = u"Center for Ocean-Land-Atmosphere Studies"
    i.CountryCode = u"US"
    i.URL = u"http://grads.iges.org/colablurb.html"
    session.insert(i)

    # CSIRO-BOM.
    i = models.Institute()
    i.Name = u"CSIRO-BOM"
    i.LongName = u"Commonwealth Scientific and Industrial Research Organization (CSIRO) and Bureau of Meteorology (BOM), Australia"
    i.CountryCode = u"AU"
    i.URL = u"http://www.csiro.au/"
    session.insert(i)

    # BCC.
    i = models.Institute()
    i.Name = u"BCC"
    i.LongName = u"Beijing Climate Center, China Meteorological Administration"
    i.CountryCode = u"CN"
    i.URL = u"http://bcc.cma.gov.cn/en/"
    session.insert(i)

    # GCESS.
    i = models.Institute()
    i.Name = u"GCESS"
    i.LongName = u"College of Global Change and Earth System Science, Beijing Normal University"
    i.CountryCode = u"CN"
    i.URL = u"http://www.bnu.edu.cn/gces/"
    session.insert(i)

    # CCCMA.
    i = models.Institute()
    i.Name = u"CCCMA"
    i.LongName = u"Canadian Centre for Climate Modelling and Analysis"
    i.CountryCode = u"CA"
    i.URL = u"http://www.ec.gc.ca/ccmac-cccma/"
    session.insert(i)

    # RSMAS.
    i = models.Institute()
    i.Name = u"RSMAS"
    i.LongName = u"University of Miami - RSMAS"
    i.CountryCode = u"US"
    i.URL = u"http://www.rsmas.miami.edu/"
    session.insert(i)

    # NCAR.
    i = models.Institute()
    i.Name = u"NCAR"
    i.LongName = u"National Center for Atmospheric Research"
    i.CountryCode = u"US"
    i.URL = u"http://ncar.ucar.edu/"
    session.insert(i)

    # NSF-DOE-NCAR.
    i = models.Institute()
    i.Name = u"NSF-DOE-NCAR"
    i.LongName = u"Community Earth System Model Contributors"
    i.CountryCode = u"US"
    i.URL = u"http://www.cesm.ucar.edu/"
    session.insert(i)

    # NCEP.
    i = models.Institute()
    i.Name = u"NCEP"
    i.LongName = u"National Centers for Environmental Prediction"
    i.CountryCode = u"US"
    i.URL = u"http://www.ncep.noaa.gov/"
    session.insert(i)

    # CMCC.
    i = models.Institute()
    i.Name = u"CMCC"
    i.LongName = u"Centro Euro-Mediterraneo per I Cambiamenti Climatici"
    i.CountryCode = u"IT"
    i.URL = u"http://www.cmcc.it/"
    session.insert(i)

    # CNRM-CERFACS.
    i = models.Institute()
    i.Name = u"CNRM-CERFACS"
    i.LongName = u"Centre National de Recherches Meteorologiques / Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique"
    i.CountryCode = u"FR"
    i.URL = u"http://www.cerfacs.fr/"
    session.insert(i)

    # CSIRO-QCCCE.
    i = models.Institute()
    i.Name = u"CSIRO-QCCCE"
    i.LongName = u"Commonwealth Scientific and Industrial Research Organisation / Queensland Climate Change Centre of Excellence"
    i.CountryCode = u"AU"
    i.URL = u"http://www.csiro.au/"
    session.insert(i)

    # EC-EARTH.
    i = models.Institute()
    i.Name = u"EC-EARTH"
    i.LongName = u"EC-EARTH"
    i.CountryCode = u"NL"
    i.URL = u"http://ecearth.knmi.nl/"
    session.insert(i)

    # LASG-CESS.
    i = models.Institute()
    i.Name = u"LASG-CESS"
    i.LongName = u"LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences and CESS,Tsinghua University"
    i.CountryCode = u"CN"
    i.URL = u"http://www.iap.ac.cn/ http://www.tsinghua.edu.cn/publish/cessen/"
    session.insert(i)

    # LASG-IAP.
    i = models.Institute()
    i.Name = u"LASG-IAP"
    i.LongName = u"LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences"
    i.CountryCode = u"CN"
    i.URL = u"http://www.iap.ac.cn/"
    session.insert(i)

    # FIO.
    i = models.Institute()
    i.Name = u"FIO"
    i.LongName = u"The First Institute of Oceanography, SOA, China"
    i.CountryCode = u"CN"
    i.URL = u"http://www.fio.org.cn/"
    session.insert(i)

    # INPE.
    i = models.Institute()
    i.Name = u"INPE"
    i.LongName = u"Instituto Nacional de Pesquisas Espaciais"
    i.CountryCode = u"BR"
    i.URL = u"http://www.inpe.br/"
    session.insert(i)

    # NASA GMAO.
    i = models.Institute()
    i.Name = u"NASA-GMAO"
    i.LongName = u"NASA Global Modeling and Assimilation Office"
    i.CountryCode = u"US"
    i.URL = u"https://gmao.gsfc.nasa.gov/"
    session.insert(i)

    # NOAA.
    i = models.Institute()
    i.Name = u"NOAA"
    i.LongName = u"National Oceanic and Atmospheric Administration"
    i.CountryCode = u"US"
    i.URL = u"http://www.noaa.gov/"
    session.insert(i)

    # NOAA-GFDL.
    i = models.Institute()
    i.Name = u"NOAA-GFDL"
    i.LongName = u"NOAA Geophysical Fluid Dynamics Laboratory"
    i.CountryCode = u"US"
    i.URL = u"http://www.gfdl.noaa.gov/"
    session.insert(i)

    # NASA GISS.
    i = models.Institute()
    i.Name = u"NASA-GISS"
    i.LongName = u"NASA Goddard Institute for Space Studies"
    i.CountryCode = u"US"
    i.URL = u"http://www.giss.nasa.gov/"
    session.insert(i)

    # NIMR-KMA.
    i = models.Institute()
    i.Name = u"NIMR-KMA"
    i.LongName = u"National Institute of Meteorological Research/Korea Meteorological Administration"
    i.CountryCode = u"KR"
    i.URL = u"http://www.nimr.go.kr/MA/main.jsp"
    session.insert(i)

    # MOHC.
    i = models.Institute()
    i.Name = u"MOHC"
    i.LongName = u"Met Office Hadley Centre"
    i.CountryCode = u"UK"
    i.URL = u"http://www.metoffice.gov.uk/climatechange/science/hadleycentre/"
    session.insert(i)

    # INM.
    i = models.Institute()
    i.Name = u"INM"
    i.LongName = u"Institute of Numerical Mathematics"
    i.CountryCode = u"RU"
    i.URL = u"http://www.inm.ras.ru/"
    session.insert(i)

    # IPSL.
    i = models.Institute()
    i.Name = u"IPSL"
    i.LongName = u"Institut Pierre Simon Laplace"
    i.CountryCode = u"FR"
    i.URL = u"http://www.ipsl.fr/"
    session.insert(i)

    # MIROC.
    i = models.Institute()
    i.Name = u"MIROC"
    i.LongName = u"Japan Agency for Marine-Earth Science and Technology, Atmosphere and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies"
    i.CountryCode = u"JP"
    i.URL = u"http://www.ccsr.u-tokyo.ac.jp/"
    session.insert(i)

    # MPI-M.
    i = models.Institute()
    i.Name = u"MPI-M"
    i.LongName = u"Max Planck Institute for Meteorology"
    i.CountryCode = u"DE"
    i.URL = u"http://www.mpimet.mpg.de/"
    session.insert(i)

    # MRI.
    i = models.Institute()
    i.Name = u"MRI"
    i.LongName = u"Meteorological Research Institute"
    i.CountryCode = u"JP"
    i.URL = u"http://www.mri-jma.go.jp/"
    session.insert(i)

    # NICAM.
    i = models.Institute()
    i.Name = u"NICAM"
    i.LongName = u"Nonhydrostatic Icosahedral Atmospheric Model Group"
    i.CountryCode = u"JP"
    i.URL = u"http://www.ccsr.u-tokyo.ac.jp/~satoh/nicam/index.html"
    session.insert(i)

    # NCC.
    i = models.Institute()
    i.Name = u"NCC"
    i.LongName = u"Norwegian Climate Centre"
    i.CountryCode = u"NO"
    i.URL = u"http://www.cicero.uio.no/"
    session.insert(i)

    # NESII.
    i = models.Institute()
    i.Name = u"NESII"
    i.LongName = u"NOAA Environmental Software Infrastructure and Interoperability Group"
    i.CountryCode = u"US"
    i.URL = u"http://www.esrl.noaa.gov/nesii"
    session.insert(i)

    # DOE.
    i = models.Institute()
    i.Name = u"DOE"
    i.LongName = u"Department of Energy"
    i.CountryCode = u"US"
    i.URL = u"http://energy.gov"
    session.insert(i)

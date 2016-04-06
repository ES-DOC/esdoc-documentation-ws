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
    i.name = u"--"
    i.long_name = u"Placeholder for scenario when an institute is undefined"
    i.country_code = u"--"
    session.insert(i)

    # Test.
    i = models.Institute()
    i.name = u"TEST"
    i.long_name = u"Placeholder for test scenrarios"
    i.country_code = u"--"
    session.insert(i)

    # BADC.
    i = models.Institute()
    i.name = u"BADC"
    i.long_name = u"British Atmospheric Data Centre"
    i.country_code = u"UK"
    i.url = u"http://badc.nerc.ac.uk/home/index.html"
    session.insert(i)

    # COLA-CFS.
    i = models.Institute()
    i.name = u"COLA-CFS"
    i.long_name = u"Center for Ocean-Land-Atmosphere Studies"
    i.country_code = u"US"
    i.url = u"http://grads.iges.org/colablurb.html"
    session.insert(i)

    # CSIRO-BOM.
    i = models.Institute()
    i.name = u"CSIRO-BOM"
    i.long_name = u"Commonwealth Scientific and Industrial Research Organization (CSIRO) and Bureau of Meteorology (BOM), Australia"
    i.country_code = u"AU"
    i.url = u"http://www.csiro.au/"
    session.insert(i)

    # BCC.
    i = models.Institute()
    i.name = u"BCC"
    i.long_name = u"Beijing Climate Center, China Meteorological Administration"
    i.country_code = u"CN"
    i.url = u"http://bcc.cma.gov.cn/en/"
    session.insert(i)

    # GCESS.
    i = models.Institute()
    i.name = u"GCESS"
    i.long_name = u"College of Global Change and Earth System Science, Beijing Normal University"
    i.country_code = u"CN"
    i.url = u"http://www.bnu.edu.cn/gces/"
    session.insert(i)

    # CCCMA.
    i = models.Institute()
    i.name = u"CCCMA"
    i.long_name = u"Canadian Centre for Climate Modelling and Analysis"
    i.country_code = u"CA"
    i.url = u"http://www.ec.gc.ca/ccmac-cccma/"
    session.insert(i)

    # RSMAS.
    i = models.Institute()
    i.name = u"RSMAS"
    i.long_name = u"University of Miami - RSMAS"
    i.country_code = u"US"
    i.url = u"http://www.rsmas.miami.edu/"
    session.insert(i)

    # NCAR.
    i = models.Institute()
    i.name = u"NCAR"
    i.long_name = u"National Center for Atmospheric Research"
    i.country_code = u"US"
    i.url = u"http://ncar.ucar.edu/"
    session.insert(i)

    # NSF-DOE-NCAR.
    i = models.Institute()
    i.name = u"NSF-DOE-NCAR"
    i.long_name = u"Community Earth System Model Contributors"
    i.country_code = u"US"
    i.url = u"http://www.cesm.ucar.edu/"
    session.insert(i)

    # NCEP.
    i = models.Institute()
    i.name = u"NCEP"
    i.long_name = u"National Centers for Environmental Prediction"
    i.country_code = u"US"
    i.url = u"http://www.ncep.noaa.gov/"
    session.insert(i)

    # CMCC.
    i = models.Institute()
    i.name = u"CMCC"
    i.long_name = u"Centro Euro-Mediterraneo per I Cambiamenti Climatici"
    i.country_code = u"IT"
    i.url = u"http://www.cmcc.it/"
    session.insert(i)

    # CNRM-CERFACS.
    i = models.Institute()
    i.name = u"CNRM-CERFACS"
    i.long_name = u"Centre National de Recherches Meteorologiques / Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique"
    i.country_code = u"FR"
    i.url = u"http://www.cerfacs.fr/"
    session.insert(i)

    # CSIRO-QCCCE.
    i = models.Institute()
    i.name = u"CSIRO-QCCCE"
    i.long_name = u"Commonwealth Scientific and Industrial Research Organisation / Queensland Climate Change Centre of Excellence"
    i.country_code = u"AU"
    i.url = u"http://www.csiro.au/"
    session.insert(i)

    # EC-EARTH.
    i = models.Institute()
    i.name = u"EC-EARTH"
    i.long_name = u"EC-EARTH"
    i.country_code = u"NL"
    i.url = u"http://ecearth.knmi.nl/"
    session.insert(i)

    # LASG-CESS.
    i = models.Institute()
    i.name = u"LASG-CESS"
    i.long_name = u"LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences and CESS,Tsinghua University"
    i.country_code = u"CN"
    i.url = u"http://www.iap.ac.cn/ http://www.tsinghua.edu.cn/publish/cessen/"
    session.insert(i)

    # LASG-IAP.
    i = models.Institute()
    i.name = u"LASG-IAP"
    i.long_name = u"LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences"
    i.country_code = u"CN"
    i.url = u"http://www.iap.ac.cn/"
    session.insert(i)

    # FIO.
    i = models.Institute()
    i.name = u"FIO"
    i.long_name = u"The First Institute of Oceanography, SOA, China"
    i.country_code = u"CN"
    i.url = u"http://www.fio.org.cn/"
    session.insert(i)

    # INPE.
    i = models.Institute()
    i.name = u"INPE"
    i.long_name = u"Instituto Nacional de Pesquisas Espaciais"
    i.country_code = u"BR"
    i.url = u"http://www.inpe.br/"
    session.insert(i)

    # NASA GMAO.
    i = models.Institute()
    i.name = u"NASA-GMAO"
    i.long_name = u"NASA Global Modeling and Assimilation Office"
    i.country_code = u"US"
    i.url = u"https://gmao.gsfc.nasa.gov/"
    session.insert(i)

    # NOAA.
    i = models.Institute()
    i.name = u"NOAA"
    i.long_name = u"National Oceanic and Atmospheric Administration"
    i.country_code = u"US"
    i.url = u"http://www.noaa.gov/"
    session.insert(i)

    # NOAA-GFDL.
    i = models.Institute()
    i.name = u"NOAA-GFDL"
    i.long_name = u"NOAA Geophysical Fluid Dynamics Laboratory"
    i.country_code = u"US"
    i.url = u"http://www.gfdl.noaa.gov/"
    session.insert(i)

    # NASA GISS.
    i = models.Institute()
    i.name = u"NASA-GISS"
    i.long_name = u"NASA Goddard Institute for Space Studies"
    i.country_code = u"US"
    i.url = u"http://www.giss.nasa.gov/"
    session.insert(i)

    # NIMR-KMA.
    i = models.Institute()
    i.name = u"NIMR-KMA"
    i.long_name = u"National Institute of Meteorological Research/Korea Meteorological Administration"
    i.country_code = u"KR"
    i.url = u"http://www.nimr.go.kr/MA/main.jsp"
    session.insert(i)

    # MOHC.
    i = models.Institute()
    i.name = u"MOHC"
    i.long_name = u"Met Office Hadley Centre"
    i.country_code = u"UK"
    i.url = u"http://www.metoffice.gov.uk/climatechange/science/hadleycentre/"
    session.insert(i)

    # INM.
    i = models.Institute()
    i.name = u"INM"
    i.long_name = u"Institute of Numerical Mathematics"
    i.country_code = u"RU"
    i.url = u"http://www.inm.ras.ru/"
    session.insert(i)

    # IPSL.
    i = models.Institute()
    i.name = u"IPSL"
    i.long_name = u"Institut Pierre Simon Laplace"
    i.country_code = u"FR"
    i.url = u"http://www.ipsl.fr/"
    session.insert(i)

    # MIROC.
    i = models.Institute()
    i.name = u"MIROC"
    i.long_name = u"Japan Agency for Marine-Earth Science and Technology, Atmosphere and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies"
    i.country_code = u"JP"
    i.url = u"http://www.ccsr.u-tokyo.ac.jp/"
    session.insert(i)

    # MPI-M.
    i = models.Institute()
    i.name = u"MPI-M"
    i.long_name = u"Max Planck Institute for Meteorology"
    i.country_code = u"DE"
    i.url = u"http://www.mpimet.mpg.de/"
    session.insert(i)

    # MRI.
    i = models.Institute()
    i.name = u"MRI"
    i.long_name = u"Meteorological Research Institute"
    i.country_code = u"JP"
    i.url = u"http://www.mri-jma.go.jp/"
    session.insert(i)

    # NICAM.
    i = models.Institute()
    i.name = u"NICAM"
    i.long_name = u"Nonhydrostatic Icosahedral Atmospheric Model Group"
    i.country_code = u"JP"
    i.url = u"http://www.ccsr.u-tokyo.ac.jp/~satoh/nicam/index.html"
    session.insert(i)

    # NCC.
    i = models.Institute()
    i.name = u"NCC"
    i.long_name = u"Norwegian Climate Centre"
    i.country_code = u"NO"
    i.url = u"http://www.cicero.uio.no/"
    session.insert(i)

    # NESII.
    i = models.Institute()
    i.name = u"NESII"
    i.long_name = u"NOAA Environmental Software Infrastructure and Interoperability Group"
    i.country_code = u"US"
    i.url = u"http://www.esrl.noaa.gov/nesii"
    session.insert(i)

    # DOE.
    i = models.Institute()
    i.name = u"DOE"
    i.long_name = u"Department of Energy"
    i.country_code = u"US"
    i.url = u"http://energy.gov"
    session.insert(i)

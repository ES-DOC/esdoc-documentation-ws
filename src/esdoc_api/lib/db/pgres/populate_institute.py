"""Populates collection of supported institutes.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.institute import Institute

# Module exports.
__all__ = ['populate_institute']



def populate_institute():
    """Populates collection of supported institutes.

    Keyword Arguments:
    session - db sesssion.
    """
    # BADC.
    i = Institute()
    i.Name = "BADC"
    i.LongName = "British Atmospheric Data Centre"
    i.CountryCode = "UK"
    i.URL = "http://badc.nerc.ac.uk/home/index.html"

    # CSIRO-BOM.
    i = Institute()
    i.Name = "CSIRO-BOM"
    i.LongName = "Commonwealth Scientific and Industrial Research Organization (CSIRO) and Bureau of Meteorology (BOM), Australia"
    i.CountryCode = "AU"
    i.URL = "http://www.csiro.au/"
    
    # BCC.
    i = Institute()
    i.Name = "BCC"
    i.LongName = "Beijing Climate Center, China Meteorological Administration"
    i.CountryCode = "CN"
    i.URL = "http://bcc.cma.gov.cn/en/"

    # GCESS.
    i = Institute()
    i.Name = "GCESS"
    i.LongName = "College of Global Change and Earth System Science, Beijing Normal University"
    i.CountryCode = "CN"
    i.URL = "http://www.bnu.edu.cn/gces/"


    # CCCMA.
    i = Institute()
    i.Name = "CCCMA"
    i.LongName = "Canadian Centre for Climate Modelling and Analysis"
    i.CountryCode = "CA"
    i.URL = "http://www.ec.gc.ca/ccmac-cccma/"
        

    # RSMAS.
    i = Institute()
    i.Name = "RSMAS"
    i.LongName = "University of Miami - RSMAS"
    i.CountryCode = "US"
    i.URL = "http://www.rsmas.miami.edu/"
    

    # NCAR.
    i = Institute()
    i.Name = "NCAR"
    i.LongName = "National Center for Atmospheric Research"
    i.CountryCode = "US"
    i.URL = "http://ncar.ucar.edu/"
    

    # NSF-DOE-NCAR.
    i = Institute()
    i.Name = "NSF-DOE-NCAR"
    i.LongName = "Community Earth System Model Contributors"
    i.CountryCode = "US"
    i.URL = "http://www.cesm.ucar.edu/"
    
    
    # NCEP.
    i = Institute()
    i.Name = "NCEP"
    i.LongName = "National Centers for Environmental Prediction"
    i.CountryCode = "US"
    i.URL = "http://www.ncep.noaa.gov/"
    

    # CMCC.
    i = Institute()
    i.Name = "CMCC"
    i.LongName = "Centro Euro-Mediterraneo per I Cambiamenti Climatici"
    i.CountryCode = "IT"
    i.URL = "http://www.cmcc.it/"
    

    # CNRM-CERFACS.
    i = Institute()
    i.Name = "CNRM-CERFACS"
    i.LongName = "Centre National de Recherches Meteorologiques / Centre Europeen de Recherche et de Formation Avancee en Calcul Scientifique"
    i.CountryCode = "FR"
    i.URL = "http://www.cerfacs.fr/"
    

    # CSIRO-QCCCE.
    i = Institute()
    i.Name = "CSIRO-QCCCE"
    i.LongName = "Commonwealth Scientific and Industrial Research Organisation / Queensland Climate Change Centre of Excellence"
    i.CountryCode = "AU"
    i.URL = "http://www.csiro.au/"
    

    # EC-EARTH.
    i = Institute()
    i.Name = "EC-EARTH"
    i.LongName = "EC-EARTH"
    i.CountryCode = "NL"
    i.URL = "http://ecearth.knmi.nl/"
    

    # LASG-CESS.
    i = Institute()
    i.Name = "LASG-CESS"
    i.LongName = "LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences and CESS,Tsinghua University"
    i.CountryCode = "CN"
    i.URL = "http://www.iap.ac.cn/ http://www.tsinghua.edu.cn/publish/cessen/"
    

    # LASG-IAP.
    i = Institute()
    i.Name = "LASG-IAP"
    i.LongName = "LASG, Institute of Atmospheric Physics, Chinese Academy of Sciences"
    i.CountryCode = "CN"
    i.URL = "http://www.iap.ac.cn/"
    

    # FIO.
    i = Institute()
    i.Name = "FIO"
    i.LongName = "The First Institute of Oceanography, SOA, China"
    i.CountryCode = "CN"
    i.URL = "http://www.fio.org.cn/"
    

    # INPE.
    i = Institute()
    i.Name = "INPE"
    i.LongName = "Instituto Nacional de Pesquisas Espaciais"
    i.CountryCode = "BR"
    i.URL = "http://www.inpe.br/"
    

    # NASA GMAO.
    i = Institute()
    i.Name = "NASA-GMAO"
    i.Synonym = "NASA GMAO"
    i.LongName = "NASA Global Modeling and Assimilation Office"
    i.CountryCode = "US"
    i.URL = "https://gmao.gsfc.nasa.gov/"
    

    # NOAA-GFDL.
    i = Institute()
    i.Name = "NOAA-GFDL"
    i.Synonym = "NOAA GFDL"
    i.LongName = "NOAA Geophysical Fluid Dynamics Laboratory"
    i.CountryCode = "US"
    i.URL = "http://www.gfdl.noaa.gov/"
    

    # NASA GISS.
    i = Institute()
    i.Name = "NASA GISS"
    i.Synonym = "NASA-GISS"
    i.LongName = "NASA Goddard Institute for Space Studies"
    i.CountryCode = "US"
    i.URL = "http://www.giss.nasa.gov/"
    

    # NIMR-KMA.
    i = Institute()
    i.Name = "NIMR-KMA"
    i.Synonym = "NIMR/KMA"
    i.LongName = "National Institute of Meteorological Research/Korea Meteorological Administration"
    i.CountryCode = "KR"
    i.URL = "http://www.nimr.go.kr/MA/main.jsp"
    

    # MOHC.
    i = Institute()
    i.Name = "MOHC"
    i.LongName = "Met Office Hadley Centre"
    i.CountryCode = "UK"
    i.URL = "http://www.metoffice.gov.uk/climatechange/science/hadleycentre/"
    

    # INM.
    i = Institute()
    i.Name = "INM"
    i.LongName = "Institute of Numerical Mathematics"
    i.CountryCode = "RU"
    i.URL = "http://www.inm.ras.ru/"
    

    # IPSL.
    i = Institute()
    i.Name = "IPSL"
    i.LongName = "Institut Pierre Simon Laplace"
    i.CountryCode = "FR"
    i.URL = "http://www.ipsl.fr/"
    

    # MIROC.
    i = Institute()
    i.Name = "MIROC"
    i.LongName = "Japan Agency for Marine-Earth Science and Technology, Atmosphere and Ocean Research Institute (The University of Tokyo), and National Institute for Environmental Studies"
    i.CountryCode = "JP"
    i.URL = "http://www.ccsr.u-tokyo.ac.jp/"
    
    
    # MPI-M.
    i = Institute()
    i.Name = "MPI-M"
    i.LongName = "Max Planck Institute for Meteorology"
    i.CountryCode = "DE"
    i.URL = "http://www.mpimet.mpg.de/"
    

    # MRI.
    i = Institute()
    i.Name = "MRI"
    i.LongName = "Meteorological Research Institute"
    i.CountryCode = "JP"
    i.URL = "http://www.mri-jma.go.jp/"
    

    # NICAM.
    i = Institute()
    i.Name = "NICAM"
    i.LongName = "Nonhydrostatic Icosahedral Atmospheric Model Group"
    i.CountryCode = "JP"
    i.URL = "http://www.ccsr.u-tokyo.ac.jp/~satoh/nicam/index.html"
    

    # NCC.
    i = Institute()
    i.Name = "NCC"
    i.LongName = "Norwegian Climate Centre"
    i.CountryCode = "NO"
    i.URL = "http://www.cicero.uio.no/"
    


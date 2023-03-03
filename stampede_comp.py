from pylib import *

# Check the atmospheric forcing (wind - sflux in netcdf format - either interpolate multiple stations for comparison, or pick the closest station) compared to observations - same method as comparison of results 
# The SCHISM input files are located in sflux as .nc format, pull points from the grid using pylibs (ReadNC: read netcdf file content as zdata format and C.VINFO) compare to the NDBC station data, starting around the inlets. 

nc=ReadNC('/scratch/08304/tg876033/RUN02b/sflux/sflux_air_1.0001.nc')  
nc.VINFO #show variable informat

#get variable values

lat = array(nc.lat.val)
lon = array(nc.lon.val)
time = array(nc.time.val)
uwind = array(nc.uwind.val)
vwind = array(nc.vwind.val)

# load the station information

# Station HCGN7 - 8654467 - USCG Station Hatteras, NC
# 35.209 N 75.704 W (35°12'31" N 75°42'15" W)

# make a figure comparing the two

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

from pylib import *

# Check the atmospheric forcing (wind - sflux in netcdf format - either interpolate multiple stations for comparison, or pick the closest station) compared to observations - same method as comparison of results 
# The SCHISM input files are located in sflux as .nc format, pull points from the grid using pylibs (ReadNC: read netcdf file content as zdata format and C.VINFO) compare to the NDBC station data, starting around the inlets. 

C=ReadNC('/scratch/08304/tg876033/RUN02b/sflux/sflux_air_1.0001.nc')  
C.VINFO #show variable informat

#get variable values

lat = array(C.lat.val)
lon = array(C.lon.val)
time = array(C.time.val)
uwind = array(C.uwind.val)
vwind = array(C.vwind.val)

# load the station information

# make a figure comparing the two

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

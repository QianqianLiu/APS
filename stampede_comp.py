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

#x=array(C.lon.val)
#y=array(C.lat.val)
#elev=array(C.elev.val)

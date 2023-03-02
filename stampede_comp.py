from pylibs import *

# Check the atmospheric forcing (wind - sflux in netcdf format - either interpolate multiple stations for comparison, or pick the closest station) compared to observations - same method as comparison of results 
# The SCHISM input files are located in sflux as .nc format, pull points from the grid using pylibs (ReadNC: read netcdf file content as zdata format and C.VINFO) compare to the NDBC station data, starting around the inlets. 

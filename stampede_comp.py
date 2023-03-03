from pylib import *
import numpy
# may need to import numpy

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

lon_sta, lat_sta = -75.704, 35.209
distance = (lon - lon_sta)**2 + (lat - lat_sta)**2
indx, indy = numpy.where(distance==distance.min()) # find the index of the minimum distance between the lat/lon positions

indx[0] # Display index for station lon/lat in the sflux nc file data 
indy[0]

# integrate all the wind from all the sflux nc files to make a time series of wind at that index to compare. Concatenate into one time series
# make a figure comparing the two

# Three columns for each dataset - datenum/time, wind direction, speed -- convert mag and direction to uwind and vwind or other way to make consistent, then make two plots for vwind and uwind

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

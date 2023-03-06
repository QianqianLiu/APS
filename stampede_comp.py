from pylib import *
import numpy as np
from datetime import datetime, timedelta

# Check the atmospheric forcing (wind - sflux in netcdf format - either interpolate multiple stations for comparison, or pick the closest station) compared to observations - same method as comparison of results 
# The SCHISM input files are located in sflux as .nc format, pull points from the grid using pylibs (ReadNC: read netcdf file content as zdata format and C.VINFO) compare to the NDBC station data, starting around the inlets. 

nc=ReadNC('/scratch/08304/tg876033/RUN02b/sflux/sflux_air_1.0001.nc')  
nc.VINFO #show variable information

#get variable values

lat = array(nc.lat.val)
lon = array(nc.lon.val)

########################################## Load the station information ############################################

# Station HCGN7 - 8654467 - USCG Station Hatteras, NC
# 35.209 N 75.704 W (35°12'31" N 75°42'15" W)


######################################### Modify and concatenate .nc data for comparison #################################################

lon_sta, lat_sta = -75.704, 35.209 #define station coordinates 
distance = (lon - lon_sta)**2 + (lat - lat_sta)**2 # calculate the distance between the station coords and the nc file coords
indx, indy = np.where(distance==distance.min()) # find the index of the minimum distance between the lat/lon positions

indx[0] # Display index for station lon/lat in the sflux nc file data 
indy[0]

#[110, 261]

# integrate all the wind from all the sflux nc files to make a time series of wind at that index to compare. Concatenate into one time series
# make a figure comparing the two

time = array(nc.time.val) # since prev day 00:00

uwind = array(nc.uwind.val[:, 200, 261])
vwind = array(nc.vwind.val[:, 200, 261])

input_wind = np.array([time], [uwind], [vwind])

arr = np.concatenate([input_wind, column_to_be_added], axis=1)

# Three columns for each dataset - datenum/time, wind direction, speed -- convert mag and direction to uwind and vwind or other way to make consistent, then make two plots for vwind and uwind
## check for model inputs - are uwind and vwind the directions the wind is coming from, or the direction the wind is going?

########### Can we write this as a function for future datasets?

##### ncdump .nc file info ######

#float uwind(time, ny_grid, nx_grid) ;
		#uwind:long_name = "Surface Eastward Air Velocity (10m AGL)" ;
		#uwind:standard_name = "eastward_wind" ;
		#uwind:units = "m/s" ;
#float vwind(time, ny_grid, nx_grid) ;
		#vwind:long_name = "Surface Northward Air Velocity (10m AGL)" ;
		#vwind:standard_name = "northward_wind" ;
		#vwind:units = "m/s" ;
    

##### NDBC data column info ######

#WDIR	Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD. See Wind Averaging Methods
#WSPD	Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly. See Wind Averaging Methods.


###################### Matlab conversion ############################

# % Convert wind speed and direction to Ugeo and Vgeo
# RperD=pi/180;
# Ugeo2=-Wnd2.*sin(Wdir2*RperD);
# Vgeo2=-Wnd2.*cos(Wdir2*RperD);

##################### Concatenate station data (Obs) to one array for comparison ################################
sta_wind = np.array([], [], []) # Assign station data and variables to this array after editing wind dir and speed 


####################### Make a Figure ##############################
figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

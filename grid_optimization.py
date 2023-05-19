from pylib import *

## to optimize the grid, the first step is to get the high resolution DEM
## 1/9 arc second grid for the nc area:
## https://coast.noaa.gov/htdata/raster2/elevation/NCEI_ninth_Topobathy_2014_8483/
## download the files in tif format
## use the following command to convert the files to npz format used by zhengui:

#convert_dem_format('ncei19_nxxxx.tif','test.npz',fmt=1)

#Then use the commands below to convert the bathymetry files to contours
#test=loadz('test.npz')
#levels=[-5,-4,-3,-2,-1,0]
#compute_contour(test.lon,test.lat,test.elev,levels,fname='contours')
#the files will be saved as contours_m5/4/3/2/1/0.shx/dbf/prj/shp files.

#can combine multiple shapefiles


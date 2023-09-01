from pylib import *

## to optimize the grid, the first step is to get the high resolution DEM
## 1/9 arc second grid for the nc area:
## https://coast.noaa.gov/htdata/raster2/elevation/NCEI_ninth_Topobathy_2014_8483/
## download the files in tif format
## use the following command to convert the files to npz format used by zhengui:
# Then use the commands below to convert the bathymetry files to contours

import glob
tiffiles = glob.glob('../NC_DEMs/*.tif')

for of,file in enumerate(tiffiles):
    convert_dem_format(file,'../NC_DEMs/oa.npz',fmt=1)
    test=loadz('../NC_DEMs/oa.npz')
    levels=[-6, -5, -4, -3, -2, -1, 0]
    fname='../NC_DEMs/contours/contours'+str(of)
    compute_contour(test.lon,test.lat,test.elev,levels,fname=fname)

import pandas as pd
import geopandas as gpd


#cfiles = glob.glob('../NC_DEMs/contours/contour*_m0.shp')

for le in levels:
    cfiles = glob.glob('../NC_DEMs/contours/contour*_m{}.shp'.format(abs(le)))
    for i,cfile in enumerate(cfiles):
        gdfi = gpd.read_file(cfile)
        if i==0:
            gdf=gdfi
        else:
            gdf = gpd.GeoDataFrame(pd.concat([gdf,gdfi]))

    gdf.to_file('../NC_DEMs/contour_m{}.shp'.format(abs(le)))

#the files will be saved as contours0/1/2/3/4/5/6_m5/4/3/2/1/0.shx/dbf/prj/shp files.
#can combine multiple shapefiles


#!/usr/bin/env python3
from pylib import *

sms2grd('APS_Merged_Jul28_2022.2dm','hgrid.gr3')

gd = read_schism_hgrid("hgrid.gr3")
#gd.lon, gd.lat = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")
gd.lon,gd.lat=gd.x,gd.y
gd.x, gd.y = proj_pts(gd.lon, gd.lat,"epsg:4326", "epsg:26918")

#method 1: if value is not given, gd.dp is used for default value
gd.write_hgrid('hgrid.gr3_new')
gd.write_hgrid('hgrd.ll')
##gd.write_hgrid('data/tmp.ic')


gd.write_shapefile_bnd('data/hgrid_bnd',prj='epsg:26918')
gd.write_shapefile_node('data/hgrid_node',prj='epsg:26918')
gd.write_shapefile_element('data/hgrid_elem',prj='epsg:26918')



for i in arange(gd.nob) : #loop open bnds
    sind=gd.iobn[i]         #get bnd indices
    bxi=gd.x[sind]; byi=gd.y[sind]  #get bnd coordinate
    plot(bxi,byi,'r*-')              #plot
for i in arange(gd.nlb): #loop land bnd
    sind=gd.ilbn[i]
    bxi=gd.x[sind]; byi=gd.y[sind]
    plot(bxi,byi,'g-')

#The above code is the same as the following
figure(); gd.plot_bnd(c='rg')

gd=read_schism_hgrid('hgrid.gr3')
gd.lon, gd.lat = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")
vd=read_schism_vgrid('vgrid.in')

#save grid  information for later use
if not os.path.exists('grid.npz'): 
  S=zdata()  #get a empty data class
  S.hgrid=gd    #save grid information as an attribute of S
  S.vgrid=vd    #save grid information as an attribute of S
  savez('grid',S)  #save hgrid first


# find the position that is closest to the rivers:


# do the interpolation



# save the file to TEM_1.th








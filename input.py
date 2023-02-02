##### Generate new files for SCHISM model #####

# Before running this code, generate .2dm grid in SMS, convert to hgrid.gr3 file, and put into a new /data folder in the working experiment directory
# sms2grd('data/latest_mesh_name.2dm','data/hgrid.gr3')

####### convert hgrid.gr3 fron lon/lat to UTM coords #######
#generate lon and lat variables first

gd = read_schism_hgrid('/home/bootk/Analysis/RUN02b/data/hgrid.gr3')
gd.lon,gd.lat=gd.x,gd.y
gd.x, gd.y = proj_pts(gd.lon, gd.lat,"epsg:4326", "epsg:26918") #Reassign x and y to be points, not lon/lat coords -- now 2 sets of variables

if not os.path.exists('input'):
   os.makedirs('input')

gd.write_hgrid('input/hgrid.gr3') ## this will write the new hgrid.gr3 file

#Reverse operation
#gd.lon, gd.lat = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")
#gd.x, gd.y = proj_pts(gd.lon, gd.lat,"epsg:4326", "epsg:26918")

# 2. Create a hgrid.11 file
# tranform SCHISM grid from lat/lon to UTM

proj('input/hgrid.gr3',0,'epsg:26918','input/hgrid.ll',0,'epsg:4326')

# 3. Assign boundary points using bp prompt, note coords for each boundary
		#bxy = x1, x2, y1, y2
		#Ocean: 1.6301e5, 4.2345e5, 3.74907e6, 4.03853e6
		#Chowan: 4.011828e6, 4.013566e6, 3.47854e5, 3.46167e5
		#Roanoke: 3.979274e6, 3.978656e6, 3.44054e5, 3.45713e5
		#Pamlico: 3.931826e6, 3.929105e6, 3.17280e5, 3.16335e5
		#Neuse: 3.892039e6, 3.890990e6, 3.12039e5, 3.11462e5
		#Cape Fear: 3.791924e6, 3.792303e6, 2.28337e5, 2.28018e5

# compute the boundaries based on the x y coords --> example: gd.compute_bnd(bxy = [ [x1,x2, y1,y2], [ x1,x2, y1, y2] ] for each point

gd.compute_bnd(bxy = [[1.6301e5, 4.2345e5, 3.74907e6, 4.03853e6], [3.47854e5, 3.46167e5, 4.011828e6, 4.013566e6], [3.44054e5, 3.45713e5, 3.979274e6, 3.978656e6], [3.17280e5, 3.16335e5, 3.931826e6, 3.929105e6], [3.12039e5, 3.11462e5, 3.892039e6, 3.890990e6], [2.28337e5, 2.28018e5, 3.791924e6, 3.792303e6]])
gd.write_bnd()

#gd.write_bnd(“file path”) #** alt for dif file

# 4. Append boundaries to end of hgrid file
	
cat grd.bnd >> input/hgrid.gr3 
	
#in mac, under ipython (do this before making any plot)
mpl.use('QtAgg')

# 5. write values to gr3
# Used to generate new gr3 files including albedo.gr3,0.05000000
gd.write_hgrid('input/albedo.gr3',value=0.0500)
gd.write_hgrid('input/drag.gr3',value=0.002500)
gd.write_hgrid('input/diffmax.gr3',value=1.00000000)
gd.write_hgrid('input/diffmin.gr3',value=0.00000100)
gd.write_hgrid('input/manning.gr3',value=0.02500000)
gd.write_hgrid('input/watertype.gr3',value=1.00000)
gd.write_hgrid('input/windrot_geo2proj.gr3',value=0.00)


# 6. Also update vgrid.in: use gen_vqs.py
# check paths of grd, vgrid.in and plot
run gen_vqs.py

# 7. To run in Stampede:
# *** If permission access denied, QQ needs to allow permission using “chmod 755 foldername -R” ***
#Copy recent experiment folder to new updated folder in work directory, and replace the old with the new grid files

# —> move all needed files to to /data folder before moving entire folder to stampede
#scp -r *.nc hgrid.ll *.gr3 *.in tvd.prop tg876033@stampede2.tacc.utexas.edu:/work2/08304/tg876033/stampede2/schism/APS/Input/RUN02b

# 7. Update bctides.in for the number of nodes along the open boundaries
#### Can do this manually


# 8. Find the element number for the Pasquotank and the New River, and update them in the source_sink.in.
# (-76.17,36.28): close to the Pasquotank River mouth
# (-77.4, 34.7): close to the New River mouth
pas_x, pas_y = -76.17, 36.28
new_x, new_y = -77.4, 34.7

# compute all geometry information of hgrid
gd.compute_all()

#find nearest points of (pas_x, pas_y) in c_[gd.xctr,gd.yctr]
sindp1=near_pts(c_[pas_x,pas_y],c_[gd.xctr,gd.yctr]) # the nearest element center
sindp2=near_pts(c_[new_x,new_y],c_[gd.xctr,gd.yctr]) # the nearest element center

with open("input/source_sink.in", "w") as f:
    f.write("2 ! total # of elements with sources")
    f.write("\n")
    f.write(str(sindp1[0])+' ! Pasquotank River; element # of 1st source')
    f.write("\n")
    f.write(str(sindp2[0])+' ! New River; element # of 2st source')
    f.write("\n")
    f.write("\n")
    f.write("0")

## No need to change vsource.th, msource.th and boundary files.

# 9. In stampede, copy everything from work to scratch before running:
# cp -r /work2/06713/lqq0622/stampede2/schism/APS/Input/RUN02a RUN02a
       

# ********** We find the points where each boundary begins and ends, put into text file optional, then input to the compute boundary command
# Future: we don’t need to look up the boundary coordinates each time, just make sure to run the code again for each new .gr3 grid file. 

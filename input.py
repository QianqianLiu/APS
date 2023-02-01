##### Generate new files for SCHISM model #####

# Before running this code, generate .2dm grid in SMS, convert to hgrid.gr3 file, and put into a new /data folder in the working experiment directory
# sms2grd('data/latest_mesh_name.2dm','data/hgrid.gr3')

####### convert hgrid.gr3 fron lon/lat to UTM coords #######
#generate lon and lat variables first

gd = read_schism_hgrid(“hgrid.gr3”)
gd.lon,gd.lat=gd.x,gd.y
gd.x, gd.y = proj_pts(gd.lon, gd.lat,"epsg:4326", "epsg:26918") #Reassign x and y to be points, not lon/lat coords -- now 2 sets of variables

### Ask QQ - How to rewrite hgrid file after changing from lat/lon to UTM
#gd.write_hgrid('data/hgrid.gr3',value=0.1)

#Reverse operation
#gd.lon, gd.lat = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")
#gd.x, gd.y = proj_pts(gd.lon, gd.lat,"epsg:4326", "epsg:26918")

# 2. Create a hgrid.11 file
# tranform SCHISM grid from lat/lon to UTM

proj('data/hgrid.gr3',0,'epsg:26918','data/hgrid.ll',0,'epsg:4326')

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
	
cat grd.bnd >>hgrid.gr3 
	
#in mac, under ipython (do this before making any plot)
mpl.use('QtAgg')

# 5. write values to gr3

gd=read_schism_hgrid('data/hgrid.gr3')
gd.write_hgrid('data/tmp2.gr3',value=0.1) 

# 6. Also update vgrid.in: use gen_vqs.py

gen_vqs.py

# 7. To run in Stampede:
# *** If permission access denied, QQ needs to allow permission using “chmod 755 foldername -R” ***
#Copy recent experiment folder to new updated folder in work directory, and replace the old with the new grid files

# —> move all needed files to to /data folder before moving entire folder to stampede
#scp -r *.nc hgrid.ll *.gr3 *.in tvd.prop tg876033@stampede2.tacc.utexas.edu:/work2/08304/tg876033/stampede2/schism/APS/Input/RUN02b

# 7. Update bctides.in for the number of nodes along the open boundaries
# 8. Find the element number for the Pasquotank and the New River, and update them in the source_sink.in.
# 9. In stampede, copy everything from work to scratch before running:
# cp -r /work2/06713/lqq0622/stampede2/schism/APS/Input/RUN02a RUN02a
       

# ********** We find the points where each boundary begins and ends, put into text file optional, then input to the compute boundary command
# Future: we don’t need to look up the boundary coordinates each time, just make sure to run the code again for each new .gr3 grid file. 

# Repository for SCHISM experiment setup, output visualization and data management

Generate new input files for SCHISM experiment - input.py

We don’t need to look up the boundary coordinates each time as long as we are keeping the same boundary inputs, just make sure to run the code again for each new .gr3 grid file. 

Before running input.py 
    1. generate .2dm grid in SMS
    2. convert to hgrid.gr3 file using pylibs ** sms2gr3() ** command
            # # sms2grd('data/latest_mesh_name.2dm','data/hgrid.gr3')
    3. put grid into a new /data folder in the working experiment directory and delete/archive old grid files in a /data_old folder for reference

After running input.py

- Update bctides.in for the number of nodes along the open boundaries. #### Can do this manually

--> No need to change vsource.th, msource.th and boundary files, use previous experiment files. 

To run in Stampede:

- If permission access denied, QQ needs to allow permission using “chmod 755 foldername -R” ***

- Copy recent experiment folder to new updated folder in work directory, and replace the old with the new grid files

scp -r *.nc hgrid.ll *.gr3 *.in tvd.prop tg876033@stampede2.tacc.utexas.edu:/work2/08304/tg876033/stampede2/schism/APS/Input/RUN02b
scp -r input tg876033@stampede2.tacc.utexas.edu:/work2/08304/tg876033/stampede2/schism/APS/Input/RUN02b

######### Copy everything from work to scratch before running: ################
# cp -r /work2/06713/lqq0622/stampede2/schism/APS/Input/RUN02a RUN02a

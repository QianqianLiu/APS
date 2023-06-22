#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download NDBC data:
#-----------------------------------------------------
#read data


#--- to download data
#urllib.request.urlretrieve('https://www.ndbc.noaa.gov/view_text_file.php?filename=41025h2019.txt.gz&dir=data/historical/stdmet/','test.csv')

ddir='StationData_2019'

#read data
#fnames=os.listdir('{}'.format(ddir));
import glob
fnames=glob.glob('{}/*2019.txt'.format(ddir))
stations=[41001,41002,41013,41024,41025,41037,41038,41064,41108,41110]

station=[]; otime=[]; temp=[]
for f in arange(len(fnames)):
    fname=fnames[f]
    sta=fname.split('/')[1].split('_')[0] #get the station name

    fid=open(fname,'r'); lines=fid.readlines(); fid.close(); lines=lines[2:]
    
    for i in arange(len(lines)):
        line=lines[i].split()
        yr=line[0]; mo=line[1]; dy=line[2]; hr=line[3]; mn=line[4]
        doyi=datenum(int(yr),int(mo),int(dy),int(hr),int(mn),0)
        #wtmp=line[18]; atmp=line[17] # for water temperature and air temperature
        wtmp=float(line[14]); atmp=float(line[13]) # for water temperature and air temperature

        otime.append(doyi)
        temp.append(wtmp)
        station.append(sta)


#-save data-------
S=npz_data(); S.time=array(otime)
S.temp=array(temp) # S.salt=array(salt); S.do=array(do); S.ph=array(ph)
S.station=array(station)


# add lat&lon information
#Lat=dict(zip(C.station,C.lat)); Lon=dict(zip(C.station,C.lon))
#S.lat=array([Lat[i] for i in S.station])
#S.lon=array([Lon[i] for i in S.station])
save_npz('NDBC_NC',S)


# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::90],xls[::90]; xls[0]=xls[0]+', 2018'

pd=(S.station=='44014')
plot(S.time[pd],S.temp[pd])
setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[25,35])
title('NDBC station {}'.format(i+1))


show(block=False)
savefig('Temp_41002.png')


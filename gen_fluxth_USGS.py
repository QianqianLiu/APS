#!/usr/bin/env python3
# generate flow.th using USGS river discharge (https://waterdata.usgs.gov/nwis/rt)

from pylib import *
import pandas as pd
import numpy as np

#usgs=['USGS_02231254_RD.csv'] # USGS files (example --> https://nwis.waterservices.usgs.gov/nwis/iv/?sites=02231254&parameterCd=00060&startDT=2016-09-01T00:00:00.000-04:00&endDT=2016-11-01T23:59:59.999-04:00&siteStatus=all&format=rdb)
#'Pasquotank_0204382800_2017_2019_15min.txt'
usgs=['ChowanFlow_2013_27Apr2021.csv','Roanoke_02080500_2017_2019_15min.txt','Tar_02084000_2017_2019_daily.txt','Neuse_02091814_2017_2019_15min.txt','CapeFear_02105769_2017_2019_15min.txt','Black_02106500_2017_2019_15min.txt']
st=datenum(2018,1,1) # start time
et=datenum(2019,12,30) # end time
sname='input/flux.th' # save name
dt=900 # time step of flow.th (second)
pt=1 # check result 1:on

# Chowan River, roanoke, Tar, Neuse, Cape Fear and Black
drainageratio = np.array([1,9660/8384, 3200/2660,(3900+370+269)/3900,1,1])

#generate flux.th
ntime=arange(0,(et-st)*86400,dt) # new time window
newset=ntime.copy() # new matrix to save data
for i,file in enumerate(usgs):
    #read csv files. Chowan River is not directly from USGS    
    if file[0:6]=='Chowan':
        df = pd.read_csv('../../usgs/'+file,skiprows=0,sep=",")
        time=datenum(1900,1,1).astype('float')+df['date']
        rd=df[df.columns[1]].values.astype('float')*0.0283168
    else:
        df = pd.read_csv('../../usgs/'+file,skiprows=27,sep="\\t")
        df = df.drop([0])
        if file[0:3]=='Tar':
            time=pd.to_datetime(df['datetime']); rd=df[df.columns[7]].values.astype('float')*0.0283168;
            time= datenum(time.values.astype('str')).astype('float')
        else:
            if df['tz_cd'][1]=='EST': print('{} has EST'.format(file));df['tz_cd'][1]='Etc/GMT+4'
            #time=pd.to_datetime(df['datetime']).dt.tz_localize(df['tz_cd'][1]).dt.tz_convert('GMT')
            tz='Etc/GMT+4'
            time=pd.to_datetime(df['datetime']).dt.tz_localize(df['tz_cd'][1]).dt.tz_convert('GMT')
            rd=df[df.columns[4]].values.astype('float')*0.0283168
            time= datenum(time.values.astype('str')).astype('float')

    #subset of time and data
    fpt=(time>=st)*(time<=et+1); time=time[fpt]; rd=rd[fpt]

    #interpolate the data to new time window and add it into new matrix
    time=(time-st)*86400; time,idx=unique(time,return_index=True); rd=rd[idx]
    #interpolate and rescale river discharge based on drainage area 
    nrd = -interpolate.interp1d(time, rd)(ntime)*drainageratio[i]

    # cape fear river and black river all goes to cape fear river
    if file[0:5]=='Black': newset[:,i]=newset[:,i]+nrd; break
    newset=column_stack((newset,nrd))

# save result
np.savetxt('{}'.format(sname),newset,fmt='%f')

mond = [datenum(2018,i+1,1)-datenum(2018,1,1) for i in range(23)]
Mond=np.array(mond); mons=Mond*24*3600
datetime= num2date(mond+datenum(2018,1,1))
Datestr=[datetime[i].strftime('%Y-%m') for i in range(23)]

cols=['green','black','blue','red','lightgrey']
labels=['Chowan River', 'roanoke', 'Tar', 'Neuse', 'Cape Fear and Black']
#check result
if pt == 1:
    fs=loadtxt(sname)
    for nn in arange(shape(fs)[1]-1):
        plt.plot(fs[:,0],-fs[:,nn+1],color=cols[nn],label=labels[nn])

    plt.legend()
    xlabel('time (s)'); ylabel('River discharge (m^3/s)')
    setp(gca(),xticks=mons, xticklabels=Datestr)
    xticks(rotation=70)
    show(block=False)

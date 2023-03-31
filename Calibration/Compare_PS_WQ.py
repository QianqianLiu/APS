#!/usr/bin/env python3
from pylib import *

# coordinates of PS stations (ps1 to ps9)
lon_ps=c_[-76.47653, -76.42758,-76.34330,-76.26680,-76.20060,-76.24867,-76.22947,-76.30570,-76.37275]
lat_ps=c_[35.1201,35.15056667,35.13125,35.11841667,35.1225,35.08255,35.03205,35.02616667,35.09986667]


S=loadz('/home/bootk/Analysis/Obs/ModMon/PS_WQ_2021.npz')
mod=loadz('/home/bootk/Analysis/mod_at_ps_wq_stations.npz')

# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'

for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.temp[pd])
    plot(mod.time+datenum(2019,1,1),mod.temp[i,:])
    setp(gca(),xticks=xts,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[10,36])
    if i>=6: setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('PS WQ Sampling station {}'.format(i+1))


show(block=False)
savefig('Compare_Temp_PS_WQ_RUN02b.png')

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'
for i in arange(9):
    print(i)
    subplot(3,3,i+1)
    pd=(S.station==i+1)*(S.depthcat==1)
    plot(S.time[pd],S.salt[pd])
    plot(mod.time+datenum(2019,1,1),mod.salt[i,:])
    setp(gca(),xticks=xts,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[10,36])
    if i>=6: setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[10,36])
    title('PS WQ Sampling station {}'.format(i+1))


show(block=False)
savefig('Compare_Salt_PS_WQ_RUN02b.png')


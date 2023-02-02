#!/usr/bin/env python3
from pylib import *

# coordinates of PS stations (ps1 to ps9)

bpfile=('station_nre.bp')
bp = read_schism_bpfile(bpfile)
stations=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180]

S=loadz('../NRE_WQ_2019.npz')
mod=loadz('mod_at_nre_stations.npz')

# make a sample plot
figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'

for i,sta in enumerate([70,100,160]):#enumerate(stations[1:19:3]): #arange(0,190,10):
    print(i)
    #print(sta)
    #figure(figsize=[16, 6])
    subplot(1,3,i+1)
    #figure(figsize=[8, 3.5])
    pd=(S.station==sta)*(S.depthcat=="S")
    pdm=stations.index(sta)
    plot(S.time[pd],S.temp[pd])
    plot(mod.time+datenum(2019,1,1),mod.temp[pdm,:])
    setp(gca(),xticks=xts,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('Temp at NRE Sampling station {}'.format(sta))


show(block=False)
savefig('Temperature_NRE.png')

figure(figsize=[16, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,30)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]+', 2018'


for i,sta in enumerate([70,100,160]):#enumerate(stations[1:19:3]): #arange(0,190,10):
    print(i)
    #print(sta)
    #figure(figsize=[16, 6])
    subplot(1,3,i+1)
    #figure(figsize=[8, 3.5])
    pd=(S.station==sta)*(S.depthcat=="S")
    pdm=stations.index(sta)
    plot(S.time[pd],S.salt[pd])
    plot(mod.time+datenum(2019,1,1),mod.salt[pdm,:])
    setp(gca(),xticks=xts,xticklabels=[],xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    setp(gca(),xticks=xts,xticklabels=xls,xlim=[datenum(2019,1,1),datenum(2019,12,30)],ylim=[0,30])
    title('Salinity at NRE Sampling station {}'.format(sta))


show(block=False)
savefig('Salt_NRE.png')



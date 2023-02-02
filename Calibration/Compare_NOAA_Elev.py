#!/usr/bin/env python3

from pylib import *

# For smaller scale tidal elevation comparison, spanning during Hurricane Dorian Aug - Sept 2019. 

#obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_msl.npz")
obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_navd.npz")

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

mod = loadz("/home/liuq/Analysis/APS/RUN02a/mod_at_noaa_stations.npz")
stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];

for st,sta in enumerate(stations):
    subplot(2,3,st+1)
    ind = (obs.station == sta) *( obs.time >= datenum(2019, 9, 3) )* (obs.time < datenum(2019, 9, 12))
    oyi=obs.elev[ind]; oyi=oyi-oyi.mean()
    plot(obs.time[ind], oyi, "r-")
    myi=mod.elev[st,:]; myi=myi-myi.mean()
    plot(mod.time + datenum(2019, 1, 1) + 0 / 24, myi,"b-")
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 9, 3), datenum(2019, 9, 12)],ylim=[-1.2, 1.2])
    title("elev. comparison at NOAA "+str(sta))

show(block=False)

savefig('Compare_Elev.png')



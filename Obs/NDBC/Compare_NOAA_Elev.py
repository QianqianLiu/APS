#!/usr/bin/env python3

from pylib import *


msl = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_msl.npz")

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::10],xls[::10]; xls[0]=xls[0]+', 2018'

mod = loadz("/home/liuq/Analysis/APS/RUN02a/mod_at_noaa_stations.npz")
stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];

station_names= ['JMPN7 - Wrightsville Beach, NC','HCGN7 - USCG Station Hatteras, NC','ORIN7 - Oregon Inlet Marina, NC','DUKN7 - Duck Pier, NC'];

#8658120 (WLON7, Wilmington, NC),
#8658163 (JMPN7, Wrightsville Beach, NC),
#8656483 (BFTN7 Beaufort, NC),
#8654467 (HCGN7, USCG Station Hatteras, NC),
#8652587 (ORIN7, Oregon Inlet Marina, NC), and
#8651370 (DUKN7, Duck Pier, NC).

station_pick = [8658163, 8654467, 8652587, 8651370];
for st,sta in enumerate(station_pick):
    subplot(2,2,st+1)
    ind = (msl.station == sta) *( msl.time >= datenum(2019, 8, 3) )* (msl.time < datenum(2019, 9, 12))
    oyi=msl.elev[ind]; oyi=oyi-oyi.mean()
    plot(msl.time[ind], oyi, "c-")
    
    ind2=(stations==sta) #### error here
    myi=mod.elev[ind2,:]; myi=myi-myi.mean()
    plot(mod.time + datenum(2019, 1, 1) + 8 / 24, myi,"k-")
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 8, 3), datenum(2019, 9, 12)],ylim=[-1.2, 1.2])
    title("Station "+str(station_names[st]))
    plt.tight_layout()
    plt.suptitle('Elevation Comparison at NOAA Stations - RUN02A', fontsize = 20)

show(block=False)
savefig('/home/bootk/Analysis/APS/Obs/ElevComp_NOAAStations.png')


#!/usr/bin/env python3

from pylib import *

# For smaller scale tidal elevation comparison, spanning during Hurricane Dorian Sept 4-12, 2019. 

#obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_msl.npz")
obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_navd.npz")

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,8,1),datenum(2019,10,1)],str='%d/%b')
xts,xls=xts[::2],xls[::2]; xls[0]=xls[0]+', 2018'

mod = loadz("/home/liuq/Analysis/APS/RUN02a/mod_at_noaa_stations.npz")
stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];

station_names= ['WLON7, Wilmington, NC','JMPN7 - Wrightsville Beach, NC','BFTN7 Beaufort, NC','HCGN7 - USCG Station Hatteras, NC','ORIN7 - Oregon Inlet Marina, NC','DUKN7 - Duck Pier, NC'];

#8658120 (WLON7, Wilmington, NC),
#8658163 (JMPN7, Wrightsville Beach, NC),
#8656483 (BFTN7 Beaufort, NC),
#8654467 (HCGN7, USCG Station Hatteras, NC),
#8652587 (ORIN7, Oregon Inlet Marina, NC), and
#8651370 (DUKN7, Duck Pier, NC).

for st,sta in enumerate(stations):
    subplot(2,3,st+1)
    ind = (obs.station == sta) *( obs.time >= datenum(2019, 9, 3) )* (obs.time < datenum(2019, 9, 12))
    oyi=obs.elev[ind]; oyi=oyi-oyi.mean()
    plot(obs.time[ind], oyi, "r-")
    myi=mod.elev[st,:]; myi=myi-myi.mean()
    plot(mod.time + datenum(2019, 1, 1) + 0 / 24, myi,"b-")
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 9, 3), datenum(2019, 9, 12)],ylim=[-1.2, 1.2])
    title("Station "+str(station_names[st]))
    plt.tight_layout()
    plt.suptitle('Elevation Comparison at NOAA Stations - September 2019', fontsize = 20)

show(block=False)

savefig('Compare_Elev_Sept.png')



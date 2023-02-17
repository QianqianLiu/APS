from pylib import *

obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_navd.npz")

figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]#+', 2018'# orig 2, not 60

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
    ind = (obs.station == sta) *( obs.time >= datenum(2019, 1, 1) )* (obs.time < datenum(2019, 12, 31))
    oyi=obs.elev[ind]; oyi=oyi-oyi.mean()
    plot(obs.time[ind], oyi, "r-")
    myi=mod.elev[st,:]; myi=myi-myi.mean()
    plot(mod.time + datenum(2019, 1, 1) + 00 / 24, myi,"b-") #orig 00 / 24
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 1, 1), datenum(2019, 12, 31)],ylim=[-1.2, 1.2])
    title("Station "+str(station_names[st]))
    plt.tight_layout()
    plt.suptitle('Elevation Comparison at NOAA Stations - 2019', fontsize = 20)

show(block=False)

savefig('Compare_Elev_2019.png')


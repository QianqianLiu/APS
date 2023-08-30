from pylib import *

# Load obs station data
#obs = loadz("/home/liuq/Analysis/APS/database_Zhengui/elev/noaa_elev_navd.npz")

obs = loadz("/home/liuq/APS/Obs/NDBC/NDBC_NC_ocean.npz")

#Create figure
figure(figsize=[15, 6])
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%d/%b')
xts,xls=xts[::60],xls[::60]; xls[0]=xls[0]#+', 2018'# orig 2, not 60

# Load model output data from station points; change address accordingly; this information needs to be extracted (pextract + stations.bp) before running this code!

mod = loadz("/home/liuq/stampede2_schism_run/Analysis/RUN02c/mod_at_noaa_salt.npz")
#stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370]; # NDBC Station numbers used for comparison

stations= ['41037','41024','41064'];

# String of station names, same order as numbers, for figure labelling later

station_names= ['ILM3 - Wrightsville Beach Offshore', 'SUN2 - Sunset Nearshore', 'LEJ3 - Onslow Bay Outer'];

#41024 ILM3 - Wrightsville Beach Offshore # 41024 is SUN2
#41037 SUN2 - Sunset Nearshore ## 41037 is ILM3
#41064 LEJ3 - Onslow Bay Outer

# Plot comparison
# 3 total stations

for st,sta in enumerate(stations): 
    subplot(3,1,st+1)
    ind = (obs.station == sta) * ( obs.time >= datenum(2019, 1, 1) ) * (obs.time < datenum(2019, 12, 31)) # define station observations from 01/01 to 12/31 in 2019
    oyi=obs.salt[ind]; #oyi=oyi-oyi.mean() # Assign the salinity observations (was elev, changed to salt) 
    plot(obs.time[ind], oyi, "r-") # plot salinity observations
    myi=mod.salt[st,:]; # myi=myi-myi.mean() # define model elevations
    plot(mod.time + datenum(2018, 1, 1) + 00 / 24, myi,"b-") # plot model time (x) every 24 hours (??) with filtered elevation (y) as blue line
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 1, 1), datenum(2019, 12, 31)],ylim=[25, 37])
    title("Station "+str(station_names[st]))
    plt.tight_layout()
    plt.suptitle('Salinity Comparison at NOAA Stations - 2019 - RUN02b', fontsize = 20)

show(block=False)

#<<<<<<< HEAD
#savefig('Compare_newSalt_2019.png')
#=======
#savefig('Compare_newSalt_2019_RUN02b.png')
#>>>>>>> e30840967c5adef90fd0f41c4aefe233a92c7285


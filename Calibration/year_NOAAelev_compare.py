from pylib import *

# Load obs station data
obs = loadz("/home/bootk/git_liu/APS/Obs/extract_noaa_sta_msl/noaa_elev_navd.npz")

# Define the years to extract and compare
years = [2002, 2019]

#Create figure
figure(figsize=[15, 6])

# Set the x axis "times" based on one year (will display ad day/month as per str.
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%b')

# Only show values/x axis points every 60 rows/2 months?? 
xts,xls=xts[::60],xls[::60]; 

# This line supposedly redundant according to ChatGPT
#xls[0]=xls[0]

# List of NDBC stations for comparison

stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];

# String of station names, same order as numbers, for figure labelling later

station_names= ['WLON7, Wilmington, NC','JMPN7 - Wrightsville Beach, NC','BFTN7 Beaufort, NC','HCGN7 - USCG Station Hatteras, NC','ORIN7 - Oregon Inlet Marina, NC','DUKN7 - Duck Pier, NC'];

#8658120 (WLON7, Wilmington, NC),
#8658163 (JMPN7, Wrightsville Beach, NC),
#8656483 (BFTN7 Beaufort, NC),
#8654467 (HCGN7, USCG Station Hatteras, NC),
#8652587 (ORIN7, Oregon Inlet Marina, NC), and
#8651370 (DUKN7, Duck Pier, NC).

# Plot comparison
# 6 total stations

for st,sta in enumerate(stations): 
    subplot(2,3,st+1)
	
    # define station observations from 01/01 - 12/31, 2019
    ind = (obs.station == sta) * ( obs.time >= datenum(2019, 1, 1) ) * (obs.time < datenum(2019, 12, 31))

    oyi=obs.elev[ind]; oyi=oyi-oyi.mean() # Assign the elevation observations 

##### Error here for lpfilt
    foyi = lpfilt(oyi,1/24,0.2) # low pass filter on observation data -- 1/24 is hourly converted to daily
    
    # Alternative smooth filter - not used
    #soyi = smooth(oyi, 24)
    
    # plot filtered observations time (x) versus elev(y) as red line
    
    # plot(obs.time[ind], oyi, "r-") 
    plot(obs.time[ind], foyi, "b-")
    #plot(obs.time[ind], soyi, "r-") # Plot smoothed obs - green line
    
    ######################## Plot model outputs (extracted previously)##############
    
    #myi=mod.elev[st,:]; myi=myi-myi.mean() # define model elevations
    #fmyi = lpfilt(myi,1/24,0.2) # Low pass filter on model data
    #smyi = smooth(myi, 24) # smooth filter on model data
    #plot(mod.time + datenum(2019, 1, 1) + 00 / 24, fmyi,"b-") # plot model time (x) every 24 hours (??) with filtered elevation (y) as blue line
    
# Observations always use UTC, but model used local time, however we changed model to UTC so there is no longer a 4 hour lag

#plot(mod.time + datenum(2019, 1, 1) + 00 / 24, smyi,"g-") # plot model time (x) every 24 hours (??) with smoothed elevation (y) as green line
    setp(gca(),xticks=xts, xticklabels=xls, xlim=[datenum(2019, 1, 1), datenum(2019, 12, 31)],ylim=[-.4, .6])
    plt.xticks(rotation=315)
    title("Station "+str(station_names[st]))
    plt.tight_layout()
    plt.suptitle(f'Elevation Comparison at NOAA Stations {years[0]} and {years[1]}', fontsize=20)

show(block=False)

#<<<<<<< HEAD
#savefig('Compare_Elev_lpfilt_2019.png')
#=======
#savefig('wl_compare_2002_2019.png')
#>>>>>>> e30840967c5adef90fd0f41c4aefe233a92c7285


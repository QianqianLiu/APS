from pylib import *

# Define the years to extract and compare
years = [2002, 2019]

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

# Load obs station data
obs = loadz("/home/bootk/git_liu/APS/Obs/extract_noaa_sta_msl/noaa_elev_navd.npz")
#Create figure
figure(figsize=[15, 6])
# Set the x axis "times" based on one year (will display ad day/month as per str.
xts,xls=get_xtick(fmt=2,xts=[datenum(2019,1,1),datenum(2019,12,31)],str='%b')
# Only show values/x axis points every 60 rows/2 months?? 
xts,xls=xts[::60],xls[::60]; 

# Plot comparison for  6 total stations

for st, sta in enumerate(stations):
    subplot(2, 3, st + 1)

    # Define station observations from 01/01 - 12/31, 2019
   
    ind_19 = (obs.station == sta) & (obs.time >= datenum(2019, 1, 1)) & (obs.time < datenum(2019, 12, 31))
    oyi_19 = obs.elev[ind_19]
    oyi_19 = oyi_19 - oyi_19.mean()  # Assign the elevation observations for 19

    foyi_19 = lpfilt(oyi_19, 1 / 24, 0.2)  # Low-pass filter on 19 observation data

    # Plot 19 data
    plot(obs.time[ind_19], foyi_19, "b-", label='2019')

    # Define station observations from 01/01 - 12/31, 2002
    
    ind_02 = (obs.station == sta) & (obs.time >= datenum(2002, 1, 1)) & (obs.time < datenum(2002, 12, 31))
    oyi_02 = obs.elev[ind_02]
    
    if oyi_02.size == 0:
        print(f"No station data for 2002 at station {sta}")
    else:
        oyi_02 = oyi_02 - oyi_02.mean()  # Assign the elevation observations for 2002
        foyi_02 = lpfilt(oyi_02, 1 / 24, 0.2)  # Low-pass filter on 2002 observation data
        plot(obs.time[ind_02], oyi_02, "r-", label='2002 Raw')
        #plot(obs.time[ind_02], foyi_02, "r-", label='2002')
        print('Size of oyi_02:', oyi_02.size)

    setp(gca(), xticks=xts, xticklabels=xls, xlim=[datenum(2019, 1, 1), datenum(2019, 12, 31)], ylim=[-0.4, 0.6])
    plt.xticks(rotation=315)
    title("Station " + str(station_names[st]))
    plt.tight_layout()
    plt.legend()
    plt.suptitle(f'Elevation Comparison at NOAA Stations {years[0]} and {years[1]}', fontsize=20)

show(block=False)



#<<<<<<< HEAD
#savefig('Compare_Elev_lpfilt_2019.png')
#=======
#savefig('wl_compare_2002_2019.png')
#>>>>>>> e30840967c5adef90fd0f41c4aefe233a92c7285


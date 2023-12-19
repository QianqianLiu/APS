#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download NOAA elevation data:  NAVD and MSL
#-----------------------------------------------------
#input
years=[2001,2019]
datums=['navd','msl'] # navd and msl are two different datums. navd is nvad88
station_list='/home/liuq/Analysis/APS/database_Zhengui/elev/stations.txt'

#noaa web link: if download not work, check this
url0='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&time_zone=GMT&units=metric&format=csv'

#read all station info
C=npz_data(); C.lon,C.lat,C.station=x=loadtxt(station_list,skiprows=1).T
C.station=C.station.astype('int')


fp = (C.lat > 34.0) * (C.lat < 36.5)
C.lon, C.lat, C.station = C.lon[fp], C.lat[fp], C.station[fp]

gd = read_schism_hgrid("/home/bootk/git_liu/APS/input/hgrid.gr3")
gd.lon, gd.lat = proj_pts(gd.x, gd.y, "epsg:26918", "epsg:4326")
plot(gd.lon, gd.lat, ".k")
plot(C.lon, C.lat, "^r")
show(block=False)



#download and read noaa data
for datum in datums:
    if not os.path.exists(datum): os.mkdir(datum)

    #download data
    for m,station in enumerate(C.station):
        for year in arange(years[0],years[1]+1):
            url='{}&datum={}&begin_date={}0101&end_date={}1231&station={}'.format(url0,datum.upper(),year,year,station)
            fname='{}_{}.csv'.format(station,year)

            if os.path.exists('{}/{}'.format(datum,fname)): continue
            print('download: {}, {}'.format(datum,fname))
            try:
                urllib.request.urlretrieve(url,'{}/{}'.format(datum,fname))
            except:
                pass

    #read data
    fnames=os.listdir('{}'.format(datum));
    #read each file in years
    mtime=[]; station=[]; elev=[]; iflag=0
    for fname in fnames:
        if not fname.endswith('.csv'): continue
        R=re.match('(\d+)_(\d+).csv',fname); sta=int(R.groups()[0]); year=int(R.groups()[1])

        #read data
        iflag=iflag+1; print('reading {}, {}'.format(fname,iflag))
        fid=open('{}/{}'.format(datum,fname),'r'); lines=fid.readlines(); fid.close(); lines=lines[1:]
        if len(lines)<10: continue

        #parse each line
        for i in arange(len(lines)):
            line=lines[i].split(',')
            if line[1]=='': continue
            doyi=datestr2num(line[0]); elevi=float(line[1])

            #save record
            mtime.append(doyi)
            station.append(sta)
            elev.append(elevi)

    #-save data-------
    S=npz_data(); S.time=array(mtime); S.elev=array(elev)
    S.station=array(station).astype('int')

    # add lat&lon information
    Lat=dict(zip(C.station,C.lat)); Lon=dict(zip(C.station,C.lon))
    S.lat=array([Lat[i] for i in S.station])
    S.lon=array([Lon[i] for i in S.station])
    save_npz('noaa_elev_{}'.format(datum),S)



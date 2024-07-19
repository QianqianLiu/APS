from pylib import *

#    USGS 0204382800 PASQUOTANK RIVER NEAR SOUTH MILLS, NC
#url='https://nwis.waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no=0204382800&legacy=&period=&begin_date=2018-01-01&end_date=2020-01-01'
#urlsave(url,'../../usgs/Pasquotank.csv')

#    USGS 02080500 ROANOKE RIVER AT ROANOKE RAPIDS, NC
#url='https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=02080500&legacy=&referred_module=sw&period=&begin_date=2018-01-01&end_date=2020-01-01'
#urlsave(url,'../../usgs/Poanoke.csv')

#
#url='https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=02084000&legacy=&referred_module=sw&period=&begin_date=2018-01-01&end_date=2020-01-01'
#url='https://nwis.waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no=02084000&legacy=&period=&begin_date=2018-01-01&end_date=2020-01-01'
#urlsave(url,'Tar.csv')

StartT='2017-12-30'; EndT='2020-01-01'; sname='APS_flow'

#------------------------------------------------------------------------------
#get stations to be downloaded
#------------------------------------------------------------------------------
#stations=unique(array([i.split(',')[1] for i in open('stations.txt').readlines()])) #SFBay
stations=['0204382800','02080500','02084000','02091814','02093000','02105769','02106500'] #Albemarle-Pamlico Sound
rnames=['Pasquotank','Roanoke','Tar','Neuse','New','CapeFear','Black']
y1=num2date(datenum(StartT)).year; y2=num2date(datenum(EndT)-1/24).year

#------------------------------------------------------------------------------
#download data for each station
#------------------------------------------------------------------------------
#sdir='data.{}'.format(sname); C=loadz('../stainfo.npz')
sdir='../../usgs'
if not os.path.exists(sdir): os.mkdir(sdir)
for m,station in enumerate(stations):
    #get links
    urls=['https://nwis.waterdata.usgs.gov/usa/nwis/uv/?cb_00060=on&format=rdb&site_no='+station+'&period=&begin_date='+StartT+'&end_date='+EndT,  #15-min flow
          'https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no='+station+'&period=&begin_date='+StartT+'&end_date='+EndT] #daily flow
    tags=['15min','daily']

    #download usgs flow data; first, try 15min data; if fails, then, try daily data
    for url,tag in zip(urls,tags):
        fname='{}/{}_{}_{}_{}_{}.txt'.format(sdir,rnames[m],station,y1,y2,tag) if y1!=y2 else '{}/{}_{}_{}.txt'.format(sdir,station,y1,tag)
        if fexist(fname): break
        print('download usgs flow: {}'.format(station))
        urlsave(url,fname)
        if os.path.getsize(fname)<3000: os.remove(fname)
        if fexist(fname): break


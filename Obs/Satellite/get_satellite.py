#!/usr/bin/env python3
from pylib import *

#-----------------------------------------------------
#download satellite data:
# Below is the erddap website for satellite NASA JPL Multi-scale Ultra-high Resolution SST
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41.graph?analysed_sst%5B(2019-09-14T09:00:00Z)%5D%5B(33.5):(36.5)%5D%5B(-77.5):(-74.5)%5D&.draw=surface&.vars=longitude%7Clatitude%7Canalysed_sst&.colorBar=%7C%7C%7C20%7C30%7C&.bgColor=0xffccccff
#-----------------------------------------------------

years=[2019,2019]

#ftp info
urlb='https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41.csv?analysed_sst%5B('
urle='T09:00:00Z)%5D%5B(33):(36.8)%5D%5B(-79):(-74)%5D&.draw=surface&.vars=longitude%7Clatitude%7Canalysed_sst&.colorBar=%7C%7C%7C20%7C30%7C&.bgColor=0xffccccff'

num=arange(datenum(years[0],1,1),datenum(years[1]+1,1,2))
for numi in num[-3:]: #num:
    datestr=str(num2date(numi))[0:10]
    url='{}{}{}'.format(urlb,datestr,urle)
    fname='jplMURSST_{}.csv'.format(datestr)
    print('downloading {}'.format(fname))
    urllib.request.urlretrieve(url,fname)








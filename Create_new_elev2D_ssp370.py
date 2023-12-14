#!/usr/bin/env python3

from pylib import *
import pandas as pd
from scipy.interpolate import interp1d

df=pd.read_csv('Obc_SLR_2098-2019_ssp370.txt',sep='\s+',header=None)

# datetime for the slr:
mond=[datenum(2019,i+1,1) for i in range(12)]-datenum(2019,1,1)
Mond=np.array(mond); #mons=Mond*24*3600
#datetime=num2date(Mond);

# read the elev2D.th.nc from RUN04d
fname='../RUN04d/elev2D.th.nc'
C=ReadNC(fname)
target_time=pd.array(C.time.val)/3600/24
slr_array=C.time_series.val


#interpolation_function=interp1d(append(Mond,365),append(df.iloc[0],df.iloc[0,-1]))

target_time = target_time.astype(float)

slr_array_target=slr_array+0
for noden in range(204):
    interpolation_function=interp1d(Mond,df.iloc[noden],kind='linear',fill_value='extrapolate')
    result=interpolation_function(target_time)
    slr_array_target[:,noden,:,:] +=result.reshape((2921,1,1))


import shutil
sou_path = '../RUN04d/elev2D.th.nc'
des_path='./elev2D_ssp370.th.nc'
shutil.copy(sou_path,des_path)

fname=des_path
C=ReadNC(fname)
C.time_series.val=slr_array_target

WriteNC(des_path,C)



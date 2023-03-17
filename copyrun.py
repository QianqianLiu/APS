#!/usr/bin/env python3
'''
  script to copy setup 
'''
from pylib import *

#input
base='RUN02a'
runs=['RUN02b']

#output dir
sdir='/home/liuq/schism/APS';

#copy runs
for run in runs:
    if os.path.exists(run): os.system('rm -r {}'.format(run))
    os.system("mkdir {}; cd {}; cp -a ../{}/*.* ./; rm *.out".format(run,run,base))
    os.system("cp ../{}/APS_VL ./".format(base)) # copy the schism executive
    print('copy {} => {}'.format(base,run))
    outdir='{}/{}/outputs'.format(sdir,run)
    os.system("mkdir {}".format(outdir))
    os.system("cd {}; mkdir sflux; ln -s /home/liuq/schism/APS/{}/sflux/*.* ./sflux/".format(run,'RUN01b'))

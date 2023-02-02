#!/usr/bin/env python3

from pylib import *

gd=read_schism_hgrid('hgrid.gr3')
gd.plot()

bpfile = 'station_noaa.bp'
bp = read_schism_bpfile(bpfile)
stations= [8658120, 8658163, 8656483, 8654467, 8652587, 8651370];
plot(bp.x,bp.y,'*r')
for st,sta in enumerate(stations):
    text(bp.x[st]+0.01,bp.y[st]-0.01,'NOAA '+str(sta),color='red')


bp_wq=bp
bp_wq.x=[-76.47653, -76.42758,-76.34330,-76.26680,-76.20060,-76.24867,-76.22947,-76.30570,-76.37275]
bp_wq.y=[35.1201,35.15056667,35.13125,35.11841667,35.1225,35.08255,35.03205,35.02616667,35.09986667]
stations=arange(1,10)
#plot(bp.x,bp.y,'ob')
#for st,sta in enumerate(stations):
#    text(bp.x[st]+0.01,bp.y[st]-0.01,'PS '+str(sta),color='b')


bp_nre=bp
bp_nre.x=[-77.12220, -77.0904, -77.0765, -77.0353, -77.0317, -77.0064, -76.9693, -76.9594, -76.9442, -76.9215, -76.8755, -76.8418, -76.81515, -76.7678, -76.7374, -76.6977, -76.66407, -76.5972, -76.52602 ]
bp_nre.y=[35.21060, 35.17793, 35.15330, 35.11375, 35.10972, 35.07952, 35.02465, 35.01472, 34.99860, 34.99050, 34.97660, 34.96170, 34.94888, 34.9525, 34.96610, 34.98750, 35.0144, 35.0274, 35.06413]

plot(bp_wq.x,bp_wq.y,'ob')

plot(bp_nre.x,bp_nre.y,'om')
legend(['', 'NOAA stations', 'Water Quality Stations','Neuse River Estuary Stations'])


setp(gca(),xlim=[-78,-74.5],ylim=[33.7,36.5])



savefig('ObsSites.png')



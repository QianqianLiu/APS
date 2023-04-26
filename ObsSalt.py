## For the generation of hotstart files in APS
## Let's use the hotstart files from Hycom
## Then modify the files in the sound using observations.
## Observations at NRE sites, pamlico sound water quality stations...


gd=loadz('grid.npz').hgrid; vd=loadz('grid.npz').vgrid; gd.x,gd.y=gd.lon,gd.lat

nre=loadz('/home/bootk/Analysis/Obs/ModMon/NRE_WQ_2019.npz')
ind = (nre.time >= datenum(2018, 12, 31)) * (nre.time <= datenum(2019, 1, 30))

gd.plot()
plot(nre.lon[ind],nre.lat[ind],'*r')

##nre.station[ind] stations: 0 0 20 20 30 30 50 50 60 60 70 70 100 100 120 120 140 140 160 160 180 180
##nre.depths[ind] 
##nre.salt[ind]


ps=loadz('/home/bootk/Analysis/Obs/ModMon/PS_WQ_2021.npz')
ind2 = (ps.time >= datenum(2018, 12, 31)) * (ps.time <= datenum(2019, 1, 30))
plot(ps.lon[ind2],ps.lat[ind2],'*r')









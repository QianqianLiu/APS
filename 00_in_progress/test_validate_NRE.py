#!/usr/bin/env python3
from pylib import *
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Import stations and extract points from model outputs
bpfile = 'station_nre.bp'
bp = read_schism_bpfile(bpfile)
stations = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]

S = loadz('/home/liuquncw/APS/Obs/ModMon/NRE_WQ_2019.npz')
mod = loadz('./mod_at_nre_stations.npz')
model_run_name = 'RUN04d'
model_run_descrip = '2019 Hindcast Simulation'

# Convert timesteps to datestr
mond = [datenum(2018, i + 1, 1) for i in range(23)]
Mond = np.array(mond)
mons = Mond * 24 * 3600
datetime = num2date(Mond)
Datestr = [datetime[i].strftime('%m') for i in range(23)]

# Initialize r-squared array for all stations
r_sq_df = np.full(len(stations), np.nan)

for i, sta in enumerate([20, 30, 50, 70, 100, 160]):
    print(i)

    pd = (S.station == sta) & (S.depthcat == "S")
    pdm = stations.index(sta)

    # Extract model points at same timesteps as observed
    obs_times = S.time[pd]
    mod_times = mod.time + datenum(2019, 1, 1)
    model_temps_at_observed_times = np.interp(obs_times, mod_times, mod.temp[pdm, :])

    # Calculate R-squared
    r_sq = r2_score(S.temp[pd], model_temps_at_observed_times)
    r_sq_df[pdm] = r_sq  # index into r_sq_df
    print(f"station {sta}, Temp R-Squared: {r_sq}")

# Print r-squared values for all stations
print("Final R-Squared values for all stations:")
print(r_sq_df)

# note nan values are stations not selected in enumerate

    
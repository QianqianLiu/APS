#!/bin/bash
#SBATCH -p shared
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=1   # Expanse has 128 cores per node
#SBATCH --mem=40G
#SBATCH -t 05:00:00             # Run time (hh:mm:ss)
#SBATCH -J extract_output              # Job name
#SBATCH --account=unc108               # Project
#SBATCH -o extract.o%j          # Name of stdout output file
#SBATCH -e extract.e%j          # Name of stderr error file
#SBATCH --export=ALL

##Environment
module load slurm
module load cpu/0.15.4
module load intel/19.1.1.217 
module load intel-mpi/2019.8.254
module load netcdf-c/4.7.4
module load netcdf-fortran/4.5.3
module load anaconda3/2020.11

##/home/liuquncw/schism/src/Utility/Combining_Scripts/combine_output11.exe -b 1 -e 73
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/pextract_schism_xyz_noaa.py
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/pextract_schism_xyz_noaa_salt.py
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/pextract_schism_xyz_neuse.py
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/pextract_schism_xyz_wq.py

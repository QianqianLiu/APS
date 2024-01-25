#!/bin/bash
#SBATCH -p shared
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=1   # Expanse has 128 cores per node
#SBATCH --mem=40G
#SBATCH -t 05:00:00             # Run time (hh:mm:ss)
#SBATCH -J compare_runs              # Job name
#SBATCH --account=unc108               # Project
#SBATCH -o compare.o%j          # Name of stdout output file
#SBATCH -e compare.e%j          # Name of stderr error file
#SBATCH --export=ALL

##Environment
module load slurm
module load cpu/0.15.4
module load intel/19.1.1.217 
module load intel-mpi/2019.8.254
module load netcdf-c/4.7.4
module load netcdf-fortran/4.5.3
module load anaconda3/2020.11

ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/Spatial_comparison.py
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/Spatial_pattern.py
ipython /expanse/lustre/projects/unc108/kboot/ModelResults/RUN2002_a/Sensitivity_PS_WQ.py
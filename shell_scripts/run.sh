#!/bin/bash
#SBATCH --account=unc108               # Project
#SBATCH -J run2002a              # Job name
#SBATCH -o aps.o%j          # Name of stdout output file
#SBATCH -e aps.e%j          # Name of stderr error file
#SBATCH -p compute              # Queue (partition)name
#SBATCH --nodes=2               # Number of nodes
#SBATCH --ntasks-per-node=80   # Expanse has 128 cores per node
#SBATCH -t 30:00:00             # Run time (hh:mm:ss)

##Environment
module load slurm
module load cpu/0.15.4
module load intel/19.1.1.217
module load intel-mpi/2019.8.254
module load netcdf-c/4.7.4
module load netcdf-fortran/4.5.3

mpirun -n 160 ./pschism_COMET_TVD-VL_noslip > log.out


#!/bin/bash
#PBS -q arm
#PBS -l select=4
#PBS -l walltime=00:00:30

module load cray-python/3.8.5.1
module use ~/modules/modulefiles
module load openmpi-4.1.6

mpirun -np 256 $HOME/simeng-parameter-study/xci_launcher.sh

#!/bin/bash
#PBS -q arm
#PBS -l select=10
#PBS -l walltime=6:00:00

module load cray-python/3.8.5.1
module use ~/modules/modulefiles
module load openmpi-4.1.6
pip install psutil

aprun -n 640 $HOME/simeng-parameter-study/xci_launcher.sh

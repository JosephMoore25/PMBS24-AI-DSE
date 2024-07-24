#!/bin/bash
#PBS -q arm
#PBS -l select=10:mem=500GB
#PBS -l walltime=24:00:00

module load cray-python/3.8.5.1
module use ~/modules/modulefiles
module load openmpi-4.1.6
pip install psutil
pip install pyyaml

for ((index=0; index<=190380; index+=640)); do
    aprun -n 640 $HOME/simeng-parameter-study/xci_recollect.sh $index
done

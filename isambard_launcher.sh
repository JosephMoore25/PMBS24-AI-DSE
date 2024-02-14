#!/bin/bash
#PBS -q romeq
#PBS -l select=2:ncpus=64
#PBS -l walltime=04:00:00

module purge
module load pbspro/pbspro/19.2.8.20200925072630
module load perftools-base/21.05.0
module load PrgEnv-cray/8.0.0
module load gcc/9.2.0
module load python3
module load openmpi

mpirun -N 2 ~/simeng-parameter-study/launcher.sh

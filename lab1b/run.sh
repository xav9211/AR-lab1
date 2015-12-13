#!/bin/sh

#PBS -l walltime=0:10:00
#PBS -l pmem=64mb
#PBS -q plgrid-testing
#PBS -A plgglaz2015b
#PBS -l nodes=1:ppn=12
mpiexec ./arlab1.py
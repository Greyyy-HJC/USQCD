#! /bin/bash

# mpirun -np 8 ./hmc -geom 2 2 2 1这个部分表示用了8个进程，是通过把格子分成了 2*2*2*1块（-geom 2 2 2 1） 
# export OMP_NUM_THREADS=1 这个表示每个进程（每个小块）用1个线程

export OMP_NUM_THREADS=1;
mpirun -np 8 taskset -c 0-7 ./hmc -geom 2 2 2 1  -i quench_hmc.ini.xml -o quench_hmc.out.xml > output_mpi.txt
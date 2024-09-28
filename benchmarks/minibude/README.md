Using miniBUDE commit 3d93e15b601fdbb151df64e4d24a8e966719b71f
Available at https://github.com/UoB-HPC/miniBUDE/tree/3d93e15b601fdbb151df64e4d24a8e966719b71f
Copy Makefile into the directory and then built with:

make COMPILER=ARM CC=armclang -e CFLAGS="-static -std=c99 -Wall -Ofast -ffast-math -fopenmp -march=armv8.4-a+sve -DWGSIZE=64 -fsimdmath -msve-vector-bits=scalable"
make COMPILER=GNU CC=gcc -e CFLAGS="-static -std=c99 -Wall -Ofast -ffast-math -fopenmp -DWGSIZE=64"

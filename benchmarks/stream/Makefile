CC = armclang
MARCH = armv8.4-a+sve
CFLAGS = -O3 -fopenmp -march=$(MARCH) --static -msve-vector-bits=scalable
STREAMFLAGS = -DSTREAM_ARRAY_SIZE=200000

all: stream_c.exe

stream_c.exe: stream.c
	$(CC) $(CFLAGS) $(STREAMFLAGS) stream.c -o stream_$(MARCH)

clean:
	rm -f stream_* *.o

# an example of a more complex build line for the Intel icc compiler
stream.icc: stream.c
	icc -O3 -xCORE-AVX2 -ffreestanding -qopenmp -DSTREAM_ARRAY_SIZE=80000000 -DNTIMES=20 stream.c -o stream.omp.AVX2.80M.20x.icc

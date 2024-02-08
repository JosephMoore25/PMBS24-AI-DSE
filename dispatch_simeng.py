import os 
import subprocess
import sys
import config_generator as generator

try:
    BATCH_ID = int(sys.argv[1])
    print("Batch ID = " + str(BATCH_ID))
except:
    print("Invalid argument: supply the index within the batch as an int")
    exit()

PATH = "/Users/jmoore/simeng-parameter-study"
HOME = os.path.expanduser("~")
minibude_binary_path = os.path.join(HOME, "simeng-benchmarks/binaries/miniBUDE/openmp/bude-armclang20.0-armv8.4-a+sve")
minibude_data_path = os.path.join(HOME, "miniBUDE/data/bm1/")

stream_binary_path = os.path.join(HOME, "simeng-benchmarks/binaries/STREAM/serial/stream-armclang20.0-armv8.4-a+sve")
#print(minibude_binary_path)
BENCHMARKS = {
    "minibude" : [minibude_binary_path, "-n", "64", "-i", "1", "--deck", minibude_data_path],
    "stream" : [stream_binary_path]
}


def generate_batch():
    config_file = generator.gen_random_config()
    config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
    f = open(config_dest, "w")
    f.write(config_file)
    f.close()

def dispatch_batch():
    for i in BENCHMARKS:
        config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
        #print(["simeng", config_dest, i])
        #print(["simeng", config_dest] + i)
        output_file = os.path.join(PATH, "results-buffer", i, "results-" + str(BATCH_ID) + ".txt")
        f = open(output_file, "w")
        subprocess.call(["simeng", config_dest] + BENCHMARKS[i], stdout=f)

if __name__ == "__main__":
    generate_batch()
    dispatch_batch()

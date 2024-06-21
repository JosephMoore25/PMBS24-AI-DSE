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

PATH = "/home/br-jmoore/simeng-parameter-study"
BENCHMARK_PATH_BASE="/home/br-jmoore/benchmarks/benchmark-binaries/aarch64/armclang-23/"
DATA_PATH_BASE = "/home/br-jmoore/benchmarks/benchmark-binaries/data"
HOME = os.path.expanduser("~")

minibude_binary_path = os.path.join(BENCHMARK_PATH_BASE, "minibude/minibude-omp_armclang23_armv8.4-a+sve")
minibude_data_path = os.path.join(DATA_PATH_BASE, "minibude/bm1/")

stream_binary_path = os.path.join(BENCHMARK_PATH_BASE, "stream/stream-100k_armclang23_armv8.4-a+sve")

cloverleaf_binary_path = os.path.join(BENCHMARK_PATH_BASE, "cloverleaf/cloverleaf-omp-armclang23-armv8.4-a+sve")
cloverleaf_data_path = os.path.join(DATA_PATH_BASE, "cloverleaf/clover.in")

tealeaf_binary_path = os.path.join(BENCHMARK_PATH_BASE, "tealeaf/TeaLeaf-armclang23-armv8.4+sve")

minisweep_binary_path = os.path.join(BENCHMARK_PATH_BASE, "minisweep/minisweep-omp-armclang23-armv8.4-a+sve")

BENCHMARKS = {
    "minibude" : [minibude_binary_path, "-n", "64", "-i", "1", "--deck", minibude_data_path],
    "stream" : [stream_binary_path]
    "cloverleaf": [cloverleaf_binary_path, cloverleaf_data_path],
    "tealeaf": [tealeaf_binary_path],
    "minisweep": [minisweep_binary_path, "--ncell_x", "4", "--ncell_y", "4", "--ncell_z", \
                    "4", "--ne", "1", "--na", "32", "--niterations", "1", "--nblock_z", \
                    "1", "--nthread_e", "1"]
}


def generate_batch():
    config_file = generator.gen_random_config()
    config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
    f = open(config_dest, "w")
    f.write(config_file)
    f.close()

def dispatch_batch():
    #print("TEST")
    print(BENCHMARKS)
    for i in BENCHMARKS:
        #Create directories if needed
        if not os.path.isdir(os.path.join(PATH, "results-buffer", i)):
            os.mkdir(os.path.join(PATH, "results-buffer", i))
            
        config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
        output_file = os.path.join(PATH, "results-buffer", i, "results-" + str(BATCH_ID) + ".txt")
        f = open(output_file, "w")
        subprocess.call(["simeng", config_dest] + BENCHMARKS[i], stdout=f)

if __name__ == "__main__":
    if not os.path.isdir(os.path.join(PATH, "config-buffer")):
        os.mkdir(os.path.join(PATH, "config-buffer"))
    if not os.path.isdir(os.path.join(PATH, "results-buffer")):
        os.mkdir(os.path.join(PATH, "results-buffer"))
    generate_batch()
    dispatch_batch()

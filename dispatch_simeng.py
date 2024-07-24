import os 
import subprocess
import sys
import config_generator as generator
import psutil
import signal
import time
import shlex
import yaml

USING_SST = True

try:
    BATCH_ID = int(sys.argv[1])
    INDEX_ID = int(sys.argv[2])
    #print("Batch ID = " + str(BATCH_ID))
except:
    print("Invalid argument: supply the index within the batch as an int")
    exit()

PATH = "/home/br-jmoore/simeng-parameter-study"
PATH = "C:/Users/Joseph/Documents/simeng-parameter-study/analysis"
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
    #"minibude" : [minibude_binary_path, "-n", "64", "-i", "1", "--deck", minibude_data_path],
    "stream" : [stream_binary_path, "a"],
    #"cloverleaf": [cloverleaf_binary_path, cloverleaf_data_path],
    "tealeaf": [tealeaf_binary_path, "a"],
    #"minisweep": [minisweep_binary_path, "--ncell_x", "4", "--ncell_y", "4", "--ncell_z", \
    #                "4", "--ne", "1", "--na", "32", "--niterations", "1", "--nblock_z", \
    #                "1", "--nthread_e", "1"]
}

# Function to check memory usage of a given PID
def check_memory(pid, threshold_kb):
    try:
        process = psutil.Process(pid)
        mem_usage = process.memory_info().rss / 1024  # Memory usage in KB
        if mem_usage > threshold_kb:
            print(f"Process {pid} is using too much memory: {mem_usage} KB")
            return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def generate_batch():
    config_file, original_parameters = generator.gen_random_config()
    config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
    f = open(config_dest, "w")
    f.write(config_file)
    f.close()
    sst_params = generator.gen_sst(original_parameters)
    sst_dest = os.path.join(PATH, "sst-buffer", "sst-%d.yaml" % BATCH_ID)
    with open(sst_dest, "w") as yaml_file:
        yaml.dump(sst_params, yaml_file, default_flow_style=False)
    return sst_params

def load_batch(index):
    config_file, sst_params, original_parameters = generator.read_parameters(index)
    config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
    f = open(config_dest, "w")
    f.write(config_file)
    f.close()
    #sst_params = generator.gen_sst(original_parameters)
    sst_dest = os.path.join(PATH, "sst-buffer", "sst-%d.yaml" % BATCH_ID)
    with open(sst_dest, "w") as yaml_file:
        yaml.dump(sst_params, yaml_file, default_flow_style=False)
    return sst_params


def dispatch_batch(sst_params):
    for i in BENCHMARKS:
        #Create directories if needed
        if not os.path.isdir(os.path.join(PATH, "results-buffer", i)):
            os.mkdir(os.path.join(PATH, "results-buffer", i))
            
        config_dest = os.path.join(PATH, "config-buffer", "config-%d.yaml" % BATCH_ID)
        output_file = os.path.join(PATH, "results-buffer", i, "results-" + str(BATCH_ID) + ".txt")
        f = open(output_file, "w")
        if (not USING_SST):
            process = subprocess.Popen(["simeng", config_dest] + BENCHMARKS[i], stdout=f)
        else:
            #print(sst_params)
            #sst_params = generator.gen_sst()
            model_options = " ".join([
                "--simeng_config", config_dest,
            "--bin_path", BENCHMARKS[i][0],
            "--bin_args", f"\"{' '.join(BENCHMARKS[i][1:])}\"",
            "--clw", str(sst_params["clw"]),
            "--core_clock", str(sst_params["core_clock"]),
            "--l1_latency", str(sst_params["l1_latency"]),
            "--l1_clock", str(sst_params["l1_clock"]),
            "--l1_associativity", str(sst_params["l1_associativity"]),
            "--l1_size", str(sst_params["l1_size"]),
            "--l2_latency", str(sst_params["l2_latency"]),
            "--l2_clock", str(sst_params["l2_clock"]),
            "--l2_associativity", str(sst_params["l2_associativity"]),
            "--l2_size", str(sst_params["l2_size"]),
            "--ram_timing", str(sst_params["ram_timing"]),
            "--ram_clock", str(sst_params["ram_clock"]),
            "--ram_size", str(sst_params["ram_size"])])

            model_options = f"""sst sst-config.py --model-options 
            '--simeng_config {config_dest} --bin_path {BENCHMARKS[i][0]} --bin_args "{' '.join(BENCHMARKS[i][1:])}"  --clw {sst_params["clw"]}  --core_clock {sst_params["core_clock"]}  --l1_latency {sst_params["l1_latency"]}  --l1_clock {sst_params["l1_clock"]}  --l1_associativity {sst_params["l1_associativity"]}  --l1_size {sst_params["l1_size"]}  --l2_latency {sst_params["l2_latency"]}  --l2_clock {sst_params["l2_clock"]} --l2_associativity {sst_params["l2_associativity"]}  --l2_size {sst_params["l2_size"]}  --ram_timing {sst_params["ram_timing"]}  --ram_clock {sst_params["ram_clock"]} --ram_size {sst_params["ram_size"]}'"""

            model_options = shlex.split(model_options)

            #process = subprocess.Popen(["sst", "sst-config.py", 
            #"--model-options", model_options], stdout=f)
            process = subprocess.Popen(model_options, stdout=f)

        while process.poll() is None:
            #Give 4GB headroom per simeng
            if check_memory(process.pid, 16*1024*1024):
                os.kill(process.pid, signal.SIGKILL)
                print(f"Killed process {process.pid} due to memory leak")
                print("This process had config: ")
                subprocess.call(["cat", config_dest])
                break
            time.sleep(1)  # Check every second
            
        #subprocess.call(["simeng", config_dest] + BENCHMARKS[i], stdout=f)

if __name__ == "__main__":
    if not os.path.isdir(os.path.join(PATH, "config-buffer")):
        os.mkdir(os.path.join(PATH, "config-buffer"))
    if not os.path.isdir(os.path.join(PATH, "results-buffer")):
        os.mkdir(os.path.join(PATH, "results-buffer"))
    if not os.path.isdir(os.path.join(PATH, "sst-buffer")):
        os.mkdir(os.path.join(PATH, "sst-buffer"))
    #sst_params = generate_batch()
    sst_params = load_batch(INDEX_ID)
    #dispatch_batch(sst_params)

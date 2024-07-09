import random
import math

ENABLE_SME = False


def get_config(parameters):
  config_file = f"""
Core:
  ISA: AArch64
  Simulation-Mode: outoforder
  Clock-Frequency-GHz: 2.5
  Timer-Frequency-MHz: 200
  Micro-Operations: True
  Vector-Length: {parameters["Vector-Length"]}
  {f'Streaming-Vector-Length: {parameters["Streaming-Vector-Length"]}' if ENABLE_SME else ""}
Fetch:
  Fetch-Block-Size: {parameters["Fetch-Block-Size"]}
  Loop-Buffer-Size: {parameters["Loop-Buffer-Size"]}
  Loop-Detection-Threshold: {parameters["Loop-Detection-Threshold"]}
Process-Image:
  Heap-Size: {parameters["Heap-Size"]}
  Stack-Size: {parameters["Stack-Size"]}
Register-Set:
  GeneralPurpose-Count: {parameters["GeneralPurpose-Count"]}
  FloatingPoint/SVE-Count: {parameters["FloatingPoint/SVE-Count"]}
  Predicate-Count: {parameters["Predicate-Count"]}
  Conditional-Count: {parameters["Conditional-Count"]}
Pipeline-Widths:
  Commit: {parameters["Commit"]}
  FrontEnd: {parameters["FrontEnd"]}
  LSQ-Completion: {parameters["LSQ-Completion"]}
Queue-Sizes:
  ROB: {parameters["ROB"]}
  Load: {parameters["Load"]}
  Store: {parameters["Store"]}
Branch-Predictor:
  Type: "Perceptron"
  BTB-Tag-Bits: 11
  Global-History-Length: 19
  RAS-entries: 8
L1-Data-Memory:
  Interface-Type: External
L1-Instruction-Memory:
  Interface-Type: Flat
LSQ-L1-Interface:
  Access-Latency: {parameters["Access-Latency"]}
  Exclusive: False
  Load-Bandwidth: {parameters["Load-Bandwidth"]}
  Store-Bandwidth: {parameters["Store-Bandwidth"]}
  Permitted-Requests-Per-Cycle: {parameters["Permitted-Requests-Per-Cycle"]}
  Permitted-Loads-Per-Cycle: {parameters["Permitted-Loads-Per-Cycle"]}
  Permitted-Stores-Per-Cycle: {parameters["Permitted-Stores-Per-Cycle"]}
Ports:
  0:
    Portname: Port 0
    Instruction-Group-Support:
    - INT_SIMPLE
    - INT_MUL
    - FP
    - SVE
  1:
    Portname: Port 1
    Instruction-Group-Support:
    - INT
    - FP
    - SVE
  2:
    Portname: Port 2
    Instruction-Group-Support:
    - INT_SIMPLE
    - INT_MUL
    - BRANCH
  3:
    Portname: Port 4
    Instruction-Group-Support:
    - LOAD
    - STORE_ADDRESS
  4:
    Portname: Port 5
    Instruction-Group-Support:
    - LOAD
    - STORE_ADDRESS
  5:
    Portname: Port 3
    Instruction-Group-Support:
    - STORE_DATA
  6:
    Portname: Port 6
    Instruction-Group-Support:
    - PREDICATE
Reservation-Stations:
  0:
    Size: 60
    Dispatch-Rate: 4
    Ports:
    - Port 0
    - Port 1
    - Port 2
    - Port 4
    - Port 5
    - Port 3
    - Port 6
Execution-Units:
  0:
    Pipelined: True
  1:
    Pipelined: True
  2:
    Pipelined: True
  3:
    Pipelined: True
  4:
    Pipelined: True
  5:
    Pipelined: True
  6:
    Pipelined: True
Latencies:
  0:
    Instruction-Groups:
    - INT
    Execution-Latency: 2
    Execution-Throughput: 2
  1:
    Instruction-Groups:
    - INT_SIMPLE_ARTH_NOSHIFT
    - INT_SIMPLE_LOGICAL_NOSHIFT
    - INT_SIMPLE_CVT
    Execution-Latency: 1
    Execution-Throughput: 1
  2:
    Instruction-Groups:
    - INT_MUL
    Execution-Latency: 5
    Execution-Throughput: 1
  3:
    Instruction-Groups:
    - INT_DIV_OR_SQRT
    Execution-Latency: 39
    Execution-Throughput: 39
  4:
    Instruction-Groups:
    - SCALAR_SIMPLE
    - VECTOR_SIMPLE_LOGICAL
    - SVE_SIMPLE_LOGICAL
    - VECTOR_SIMPLE_CMP
    - SVE_SIMPLE_CMP
    Execution-Latency: 4
    Execution-Throughput: 1
  5:
    Instruction-Groups:
    - FP_DIV_OR_SQRT
    Execution-Latency: 16
    Execution-Throughput: 16
  6:
    Instruction-Groups:
    - VECTOR_SIMPLE
    - SVE_SIMPLE
    - SCALAR_SIMPLE_CVT
    - FP_MUL
    - SVE_MUL
    Execution-Latency: 9
    Execution-Throughput: 1
  7:
    Instruction-Groups:
    - SVE_DIV_OR_SQRT
    Execution-Latency: 98
    Execution-Throughput: 98
  8:
    Instruction-Groups:
    - PREDICATE
    Execution-Latency: 3
    Execution-Throughput: 1
  9:
    Instruction-Groups:
    - LOAD_SCALAR
    - LOAD_VECTOR
    - STORE_ADDRESS_SCALAR
    - STORE_ADDRESS_VECTOR
    Execution-Latency: 3
    Execution-Throughput: 1
  10:
    Instruction-Groups:
    - LOAD_SVE
    - STORE_ADDRESS_SVE
    Execution-Latency: 6
    Execution-Throughput: 1
# structure
CPU-Info:
  # Set Generate-Special-Dir to True to generate the special files directory, or to False to not.
  # (Not generating the special files directory may require the user to copy over files manually)
  Generate-Special-Dir: False
  Special-File-Dir-Path: "/home/br-jmoore/SimEng/specialFiles"
  # Core-Count MUST be 1 as multi-core is not supported at this time.
  Core-Count: 1
  # Socket-Count MUST be 1 as multi-socket simulations are not supported at this time.
  Socket-Count: 1
  # SMT MUST be 1 as Simultanious-Multi-Threading is not supported at this time.
  SMT: 1
  # Below are the values needed to generate /proc/cpuinfo
  BogoMIPS: 400.00
  Features: fp asimd evtstrm sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm fcma pmull dcpop sve
  CPU-Implementer: "0x43"
  CPU-Architecture: 8
  CPU-Variant: "0x1"
  CPU-Part: "0x0af"
  CPU-Revision: 0
  # Package-Count is used to generate
  # /sys/devices/system/cpu/cpu{{0..Core-Count}}/topology/{{physical_package_id, core_id}}
  Package-Count: 1"""

  
  return config_file

def gen_random_config():
  parameters = {
  #Core
      "Vector-Length" : random.choice([i for i in range(128, 2048+1, 128)]),
      "Streaming-Vector-Length" : random.choice([2**i for i in range(0, 11+1)] if ENABLE_SME else [0]),
  #Fetch
      "Fetch-Block-Size" : random.choice([2**i for i in range(2, 11+1)]), #4 - 2048 (can go to 32k)
      "Loop-Buffer-Size" : random.choice([i for i in range(1, 512)]),
      "Loop-Detection-Threshold" : random.choice([i for i in range(1, 32)]),
  #Process Image
      "Heap-Size" : 1073741824, #random.choice([i for i in range(1024*1024, 2*1024*1024*1024, 32*1024*1024)]), #1MB - 2GB in 32MB steps
      "Stack-Size" : 1048576, #random.choice([i for i in range(32*1024, 32*1024*1024, 32*1024)]), #32KB - 32MB in 32KB steps
  #Register Set
      "GeneralPurpose-Count" : random.choice([i for i in range(38, 512+1, 8)]), # 32 - 65535
      "FloatingPoint/SVE-Count" : random.choice([i for i in range(38, 512+1, 8)]), # 32 - 65535
      "Predicate-Count" : random.choice([i for i in range(24, 512+1, 8)]), # 17 - 65535
      "Conditional-Count": random.choice([i for i in range(8, 512+1, 8)]),
  #Pipeline Widths
      "Commit" : random.choice([i for i in range(1, 64)]),
      "FrontEnd" : random.choice([i for i in range(1, 64)]),
      "LSQ-Completion": random.choice([i for i in range(1, 64)]),
  #Queue Sizes
      "ROB" : random.choice([i for i in range(4, 512, 4)]),
      "Load" : random.choice([i for i in range(4, 512, 4)]),
      "Store" : random.choice([i for i in range(4, 512, 4)]),
  #LSQ L1 Interface
      "Access-Latency" : random.choice([i for i in range(1, 10)]), #5,#random.choice([5]),
      "Load-Bandwidth" : random.choice([2**i for i in range(4, 10+1)]), #16 - 1024
      "Store-Bandwidth" : random.choice([2**i for i in range(4, 10+1)]), #16 - 1024
      "Permitted-Requests-Per-Cycle" : random.choice([i for i in range(1, 32+1)]),
      "Permitted-Loads-Per-Cycle" : random.choice([i for i in range(1, 32+1)]),
      "Permitted-Stores-Per-Cycle" : random.choice([i for i in range(1, 32+1)]),
  }

  #Ensure load/store bw large enough to load a full vector in one load
  while (parameters["Load-Bandwidth"] < max(parameters["Vector-Length"], parameters["Streaming-Vector-Length"])/8):
    parameters["Load-Bandwidth"] = random.choice([2**i for i in range(0, 10+1)])
  while (parameters["Store-Bandwidth"] < max(parameters["Vector-Length"], parameters["Streaming-Vector-Length"])/8):
    parameters["Store-Bandwidth"] = random.choice([2**i for i in range(0, 10+1)])
  
  return get_config(parameters), parameters

def gen_sst(original_parameters):
  parameters = {
    "clw" : random.choice([2**i for i in range(5, 10)]), #Between 32-512
    "core_clock" : 2,
    "l1_latency" : original_parameters["Access-Latency"], #random.choice([i for i in range(1, 10)]),
    "l1_clock" : random.choice([i/2 for i in range(1,10)]),
    "l1_associativity" : random.choice([2**i for i in range(0, 5)]), #Up to 16
    "l1_size" : random.choice([2**i for i in range(0, 12)]), #Up to 1KiB - 2MiB L1
    "l2_latency" : random.choice([i for i in range(6, 50)]),
    "l2_clock" : random.choice([i/2 for i in range(1, 10)]),
    "l2_associativity" : random.choice([2**i for i in range(0, 5)]), #Up to 16
    "l2_size" : random.choice([2**i for i in range(5, 17)]), #32KiB - 64MiB L2
    "ram_timing" : random.choice([i*10 for i in range(4, 26)]), #40-250ns
    "ram_clock" : random.choice([i/2 for i in range(1, 10)]),
    "ram_size" : 4
  }
  while (parameters["l2_size"] < parameters["l1_size"]):
    parameters["l2_size"] = random.choice([2**i for i in range(5, 17)])
  while (parameters["l2_latency"] <= parameters["l1_latency"]):
    parameters["l2_latency"] = random.choice([i for i in range(6, 50)])

  return parameters

#if __name__ == "__main__":
#  config_file, = gen_random_config()
#  f = open("random-config.yaml", "w")
#  f.write(config_file)
#  f.close()

import random
import math

ENABLE_SME = False


def get_config(parameters):
  config_file = f"""# The following resources where utilised to create the config file and naming schemes:
# https://github.com/fujitsu/A64FX

Core:
  ISA: AArch64
  Simulation-Mode: outoforder
  Clock-Frequency-GHz: 1.8
  Timer-Frequency-MHz: 100
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
  Access-Latency: 5
  Exclusive: True
  Load-Bandwidth: {parameters["Load-Bandwidth"]}
  Store-Bandwidth: {parameters["Store-Bandwidth"]}
  Permitted-Requests-Per-Cycle: {parameters["Permitted-Requests-Per-Cycle"]}
  Permitted-Loads-Per-Cycle: {parameters["Permitted-Loads-Per-Cycle"]}
  Permitted-Stores-Per-Cycle: {parameters["Permitted-Stores-Per-Cycle"]}
Ports:
  0:
    Portname: FLA
    Instruction-Support:
    - FP
    - SVE
  1:
    Portname: PR
    Instruction-Support:
    - PREDICATE
  2:
    Portname: EXA
    Instruction-Support:
    - INT_SIMPLE
    - INT_MUL
    - STORE_DATA
  3:
    Portname: FLB
    Instruction-Support:
    - FP_SIMPLE
    - FP_MUL
    - SVE_SIMPLE
    - SVE_MUL
  4:
    Portname: EXB
    Instruction-Support:
    - INT_SIMPLE
    - INT_DIV_OR_SQRT
  5:
    Portname: EAGA
    Instruction-Support:
    - LOAD
    - STORE_ADDRESS
    - INT_SIMPLE_ARTH_NOSHIFT
    - INT_SIMPLE_LOGICAL_NOSHIFT
    - INT_SIMPLE_CMP
  6:
    Portname: EAGB
    Instruction-Support:
    - LOAD
    - STORE_ADDRESS
    - INT_SIMPLE_ARTH_NOSHIFT
    - INT_SIMPLE_LOGICAL_NOSHIFT
    - INT_SIMPLE_CMP
  7:
    Portname: BR
    Instruction-Support:
    - BRANCH
Reservation-Stations:
  0:
    Size: 20
    Dispatch-Rate: 2
    Ports:
    - FLA
    - PR
    - EXA
  1:
    Size: 20
    Dispatch-Rate: 2
    Ports:
    - FLB
    - EXB
  2:
    Size: 10
    Dispatch-Rate: 1
    Ports:
    - EAGA
  3:
    Size: 10
    Dispatch-Rate: 1
    Ports:
    - EAGB
  4:
    Size: 19
    Dispatch-Rate: 1
    Ports:
    - BR
Execution-Units:
  0:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  1:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  2:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  3:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  4:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  5:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  6:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
  7:
    Pipelined: True
    Blocking-Groups:
    - INT_DIV_OR_SQRT
    - FP_DIV_OR_SQRT
    - SVE_DIV_OR_SQRT
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
    Execution-Latency: 41
    Execution-Throughput: 41
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
    Execution-Latency: 29
    Execution-Throughput: 29
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
# Indexed FMLA instructions split into 2 dependent µops. Latency increased to 15 to mimic such behaviour
# NOTE: Any changes to the capstone opcode list could invalidate the mapping between ARM instructions and the values below
  11:
    Instruction-Opcodes:
    - 1922
    - 1924
    - 1926
    - 2359
    - 2360
    - 2361
    - 2364
    - 2365
    - 2368
    - 2369
    - 2371
    - 2390
    - 2391
    - 2392
    - 2395
    - 2396
    - 2399
    - 2400
    - 2402
    - 2445
    - 2446
    - 2447
    - 2450
    - 2451
    - 2454
    - 2455
    - 2457
    - 2470
    - 2471
    - 2472
    - 2475
    - 2476
    - 2479
    - 2480
    - 2482
    - 3627
    - 3629
    - 3631
    - 3633
    - 3644
    - 3646
    - 3648
    - 3650
    - 3709
    - 3711
    - 3713
    - 3715
    - 4306
    - 4308
    - 4310
    - 4312
    - 4326
    - 4328
    - 4330
    - 4332
    - 4372
    - 4374
    - 4376
    - 4378
    - 4468
    - 4469
    - 4470
    - 4472
    - 4474
    - 4476
    - 4493
    - 4494
    - 4495
    - 4497
    - 4499
    - 4501
    - 4511
    - 4513
    - 4515
    - 4517
    - 4519
    - 4521
    - 4534
    - 4535
    - 4536
    - 4538
    - 4540
    - 4542
    - 4594
    - 4595
    - 4599
    - 4601
    - 4603
    - 4605
    - 4613
    - 4614
    - 4618
    - 4620
    - 4622
    - 4624
    - 4633
    - 4635
    - 4637
    - 4639
    - 4641
    - 4643
    - 5760
    - 5762
    - 5764
    - 5766
    - 5780
    - 5782
    - 5784
    - 5786
    - 5824
    - 5826
    - 5828
    - 5830
    Execution-Latency: 15
    Execution-Throughput: 1
# CPU-Info mainly used to generate a replica of the special (or system) file directory
# structure
CPU-Info:
  # Set Generate-Special-Dir to True to generate the special files directory, or to False to not.
  # (Not generating the special files directory may require the user to copy over files manually)
  Generate-Special-Dir: False
  Special-File-Dir-Path: "/home/br-jmoore/SimEng/specialFiles"
  # Core-Count MUST be 1 as multi-core is not supported at this time. (A64FX true value is 48)
  Core-Count: 1
  # Socket-Count MUST be 1 as multi-socket simulations are not supported at this time. (A64FX true value is 1)
  Socket-Count: 1
  # SMT MUST be 1 as Simultanious-Multi-Threading is not supported at this time. (A64FX true value is 1)
  SMT: 1
  # Below are the values needed to generate /proc/cpuinfo
  BogoMIPS: 200.00
  Features: fp asimd evtstrm sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm fcma dcpop sve
  CPU-Implementer: "0x46"
  CPU-Architecture: 8
  CPU-Variant: "0x1"
  CPU-Part: "0x001"
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
      "Heap-Size" : random.choice([i for i in range(1024*1024, 2*1024*1024*1024, 32*1024*1024)]), #1MB - 2GB in 32MB steps
      "Stack-Size" : random.choice([i for i in range(32*1024, 32*1024*1024, 32*1024)]), #32KB - 32MB in 32KB steps
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
    "ram_timing" : random.choice([i*10 for i in range(4, 260)]), #40-250ns
    "ram_clock" : random.choice([i/2 for i in range(1, 10)]),
    "ram_size" : 8
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

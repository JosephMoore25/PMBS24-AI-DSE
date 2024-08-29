import sys
import os
import pandas as pd
import dispatch_simeng
import yaml

#BATCH_SIZE = int(sys.argv[1])
RUN_INDEX = int(sys.argv[1])
PATH = dispatch_simeng.PATH
DB_NAME = os.path.join(PATH, sys.argv[2])
CONFIG_NO = int(sys.argv[3])

def get_inputs(index):
    parameters = {
    #Core
        "Vector-Length" : -1,
        "Streaming-Vector-Length" : -1,
    #Fetch
        "Fetch-Block-Size" : -1,
        "Loop-Buffer-Size" : -1,
        "Loop-Detection-Threshold" : -1,
    #Process Image
        "Heap-Size" : -1,
        "Stack-Size" : -1,
    #Register Set
        "GeneralPurpose-Count" : -1,
        "FloatingPoint/SVE-Count" : -1,
        "Predicate-Count" : -1,
        "Conditional-Count": -1,
    #Pipeline Widths
        "Commit" : -1,
        "FrontEnd" : -1,
        "LSQ-Completion": -1,
    #Queue Sizes
        "ROB" : -1,
        "Load" : -1,
        "Store" : -1,
    #LSQ L1 Interface
        "Access-Latency" : -1,
        "Load-Bandwidth" : -1,
        "Store-Bandwidth" : -1,
        "Permitted-Requests-Per-Cycle" : -1,
        "Permitted-Loads-Per-Cycle" : -1,
        "Permitted-Stores-Per-Cycle" : -1,

        "clw" : -1,
        "core_clock" : -1,
        "l1_latency" : -1,
        "l1_clock" : -1,
        "l1_associativity" : -1,
        "l1_size": -1,
        "l2_latency" : -1,
        "l2_clock" : -1,
        "l2_associativity" : -1,
        "l2_size" : -1,
        "ram_timing" : -1,
        "ram_clock" : -1,
        "ram_size" : -1
    }

    config = open(os.path.join(PATH, 'config-buffer', 'config-' + str(index) + '.yaml'))
    for i in config.readlines():
        for j in parameters:
            if j + ":" in i:
                parameters[j] = int(i.split()[-1])
    with open(os.path.join(PATH, 'sst-buffer', 'sst-' + str(index) + '.yaml'), 'r') as stream:
        data = yaml.load(stream, Loader=yaml.SafeLoader)
    for i in data:
        parameters[i] = data[i]
        
    return parameters

def get_results(index, benchmark):
    results = {
        benchmark + "_branch_executed" : -1,
        benchmark + "_branch_mispredict" : -1,
        benchmark + "_branch_missrate" : -1,
        benchmark + "_cycles" : -1,
        benchmark + "_decode_earlyFlushes" : -1,
        benchmark + "_dispatch_rsStalls" : -1,
        benchmark + "_fetch_branchStalls" : -1,
        benchmark + "_flushes" : -1,
        benchmark + "_ipc" : -1,
        benchmark + "_issue_backendStalls" : -1,
        benchmark + "_issue_frontendStalls" : -1,
        benchmark + "_issue_portBusyStalls" : -1,
        benchmark + "_lsq_loadViolations" : -1,
        benchmark + "_rename_allocationStalls" : -1,
        benchmark + "_rename_lqStalls" : -1,
        benchmark + "_rename_robStalls" : -1,
        benchmark + "_rename_sqStalls" : -1,
        benchmark + "_retired" : -1
    }
    result_file_name = os.path.join(PATH, "results-buffer", benchmark, "results-" + str(index) + ".txt")
    print(result_file_name)
    result_file = open(result_file_name)
    for i in result_file.readlines():
        if "Error from read_input" in i or "EMERGENCY SHUTDOWN" in i:
            for j in range(len(results)):
                results[j] = -1
            break
        for j in results:
            if all(k in i for k in j.split('_')[1:]) and ("cycles." not in i):
                try:
                    print(i)
                    results[j] = int(i.split()[-1].strip('%'))
                except:
                    results[j] = float(i.split()[-1].strip('%'))
    return results


columns = ["Config-no"]
data = [[CONFIG_NO]]

#for i in range(BATCH_SIZE):
#    parameters = get_inputs(i)
#    if (i == 0):
#        for j in parameters:
#            columns.append(j)
#
#    temp_data = []
#    for j in parameters:
#        temp_data.append(parameters[j])
#
#    for benchmark in dispatch_simeng.BENCHMARKS:
#        results = get_results(i, benchmark)
#        for j in results:
#            temp_data.append(results[j])
#            if (i == 0):
#                columns.append(j)
#
#
#data.append(temp_data)


parameters = get_inputs(RUN_INDEX)
for j in parameters:
    columns.append(j)
temp_data = []
for j in parameters:
    temp_data.append(parameters[j])

for benchmark in dispatch_simeng.BENCHMARKS:
    results = get_results(RUN_INDEX, benchmark)
    for j in results:
        temp_data.append(results[j])
        columns.append(j)
        
data[0] += temp_data

df = pd.DataFrame(data, columns=columns)

#print(df)
df.to_csv(DB_NAME, mode='a', index=False, header=not os.path.isfile(DB_NAME))

    #print(parameters)
    #print(results)

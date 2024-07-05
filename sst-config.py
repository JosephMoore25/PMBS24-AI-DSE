import sst
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("simeng_config") # Path to yaml config file
parser.add_argument("bin_path") # Path to executable binary
parser.add_argument("bin_args") # Args for executable binary
parser.add_argument("clw") # In bytes, original 64
parser.add_argument("core_clock") # In GHz, match core
parser.add_argument("l1_latency") # In cycles, original 4
parser.add_argument("l1_clock") # In GHz, original 2
parser.add_argument("l1_associativity") # Original 4
parser.add_argument("l1_size") # In KiB, original 1
parser.add_argument("l2_latency") # In cycles, original 10
parser.add_argument("l2_clock") # In GHz, original 1.8
parser.add_argument("l2_associativity") # Original 8
parser.add_argument("l2_size") # In KiB, original 16
parser.add_argument("ram_timing") # In ns, original 100
parser.add_argument("ram_clock") # In GHz, original 1
parser.add_argument("ram_size") # In GiB, original 8
args = parser.parse_args()

# Define the simulation components
cpu = sst.Component("core", "sstsimeng.simengcore")
cpu.addParams({
    "simeng_config_path": args.simeng_config,
    "executable_path": args.bin_path,
    "executable_args": args.bin_args,
    "clock" : args.core_clock + "GHz",
    "max_addr_memory": 2*1024*1024*1024-1,
    "cache_line_width": args.clw,
    "source": "",
    "assemble_with_source": False,
    "heap": "",
    "debug": False
})

iface = cpu.setSubComponent("memory", "memHierarchy.standardInterface")

l1cache = sst.Component("l1cache.msi", "memHierarchy.Cache")
l1cache.addParams({
    "access_latency_cycles" : args.l1_latency,
    "cache_frequency" : args.l1_clock + "Ghz",
    "replacement_policy" : "lru",
    "coherence_protocol" : "MSI",
    "associativity" : args.l1_associativity,
    "cache_line_size" : args.clw,
    "cache_size" : args.l1_size + "KiB",
    "L1" : "1",
    "debug" : 0,
    "debug_level" : 10,
    "verbose": "2"
})
l2cache = sst.Component("l2cache.msi.inclus", "memHierarchy.Cache")
l2cache.addParams({
    "access_latency_cycles" : args.l2_latency,
    "cache_frequency" : args.l2_clock + "Ghz",
    "replacement_policy" : "lru",
    "coherence_protocol" : "MSI",
    "associativity" : args.l2_associativity,
    "cache_line_size" : args.clw,
    "cache_size" : args.l2_size + "KiB",
    "debug_level" : "10",
    "debug": "1"
})
memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "clock" : args.ram_clock + "GHz",
    "backend.access_time" : args.ram_timing + "ns",
    "debug" : 0,
    "debug_level" : 10,
    "addr_range_end" : int(args.ram_size)*1024*1024*1024-1,
})
    
memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "access_time" : args.ram_timing + "ns",
    "mem_size" : args.ram_size + "GiB",
})


# Define the simulation links
link_cpu_l1cache = sst.Link("link_cpu_l1cache_link")
link_cpu_l1cache.connect( (iface, "port", "10ps"), (l1cache, "high_network_0", "10ps") )
link_l1cache_l2cache = sst.Link("link_l1cache_l2cache_link")
link_l1cache_l2cache.connect( (l1cache, "low_network_0", "100ps"), (l2cache, "high_network_0", "100ps") )
link_mem_bus = sst.Link("link_mem_bus_link")
link_mem_bus.connect( (l2cache, "low_network_0", "100ps"), (memctrl, "direct_link", "100ps") )

#!/usr/bin/env python3

import re
import sys
import typing
from arcaflow_plugin_sdk import plugin
import subprocess
from sysbench_schema import (
    SysbenchCpuInputParams,
    SysbenchMemoryInputParams,
    WorkloadResultsCpu,
    WorkloadResultsMemory,
    WorkloadError,
    sysbench_cpu_input_schema,
    sysbench_cpu_output_schema,
    sysbench_cpu_results_schema,
    sysbench_memory_input_schema,
    sysbench_memory_output_schema,
    sysbench_memory_results_schema,
)


def parse_output(output):
    output = output.replace(" ", "")
    section = None
    sysbench_output = {}
    sysbench_results = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":")
            if key[0].isdigit():
                key = "P" + key
            if value == "":
                key = re.sub(r"\((.*?)\)", "", key)
                if "options" in key or "General" in key:
                    dictionary = sysbench_output
                else:
                    dictionary = sysbench_results
                    section = key
                    dictionary[section] = {}
                continue

            if dictionary == sysbench_output:
                if "totaltime" in key:
                    value = value.replace("s", "")
                    dictionary[key] = float(value)
                elif "Totaloperations" in key:
                    to, tops = value.split("(")
                    tops = tops.replace("persecond)", "")
                    dictionary["Totaloperations"] = float(to)
                    dictionary["Totaloperationspersecond"] = float(tops)
                elif value.isnumeric():
                    dictionary[key] = float(value)
                else:
                    dictionary[key] = value

            else:
                if "latency" in key:
                    section = "Latency"
                if "(avg/stddev)" in key:
                    key = key.replace("(avg/stddev)", "")
                    avg, stddev = value.split("/")
                    dictionary[section][key] = {}
                    dictionary[section][key]["avg"] = float(avg)
                    dictionary[section][key]["stddev"] = float(stddev)
                elif value.isnumeric():
                    dictionary[section][key] = float(value)
                else:
                    dictionary[section][key] = value
        if "transferred" in line:
            mem_t, mem_tps = line.split("transferred")
            mem_tps = re.sub("[()]", "", mem_tps)
            mem_t = float(mem_t.replace("MiB", ""))
            mem_tps = float(mem_tps.replace("MiB/sec", ""))

            sysbench_results["transferred_MiB"] = mem_t
            sysbench_results["transferred_MiBpersec"] = mem_tps
    print("sysbench output : ", sysbench_output)
    print("sysbench results:", sysbench_results)
    return sysbench_output, sysbench_results


def run_sysbench(params, flags, operation):
    try:
        cmd = ["sysbench"]
        cmd = cmd + flags + [operation, "run"]
        process_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        raise Exception(
            error.returncode,
            "{} failed with return code {}:\n{}".format(
                error.cmd[0], error.returncode, error.output
            ),
        ) from error

    stdoutput = process_out.strip().decode("utf-8")

    try:
        output, results = parse_output(stdoutput)
    except (KeyError, ValueError) as error:
        raise Exception(
            1, "Failure in parsing sysbench output:\n{}".format(stdoutput)
        ) from error

    return output, results


@plugin.step(
    id="sysbenchcpu",
    name="Sysbench CPU Workload",
    description="Run CPU performance test using the sysbench workload",
    outputs={"success": WorkloadResultsCpu, "error": WorkloadError},
)
def RunSysbenchCpu(
    params: SysbenchCpuInputParams,
) -> typing.Tuple[str, typing.Union[WorkloadResultsCpu, WorkloadError]]:

    print("==>> Running sysbench CPU workload ...")

    serialized_params = sysbench_cpu_input_schema.serialize(params)

    cpu_flags = []
    for param, value in serialized_params.items():
        cpu_flags.append(f"--{param}={value}")

    try:
        output, results = run_sysbench(params, cpu_flags, "cpu")
    except Exception as error:
        return "error", WorkloadError(error.args[0], error.args[1])

    print("==>> Workload run complete!")

    return "success", WorkloadResultsCpu(
        sysbench_cpu_output_schema.unserialize(output),
        sysbench_cpu_results_schema.unserialize(results),
    )


@plugin.step(
    id="sysbenchmemory",
    name="Sysbench Memory Workload",
    description=(
        "Run the Memory functions speed test using the sysbench workload"
    ),
    outputs={"success": WorkloadResultsMemory, "error": WorkloadError},
)
def RunSysbenchMemory(
    params: SysbenchMemoryInputParams,
) -> typing.Tuple[str, typing.Union[WorkloadResultsMemory, WorkloadError]]:

    print("==>> Running sysbench Memory workload ...")

    serialized_params = sysbench_memory_input_schema.serialize(params)

    memory_flags = []
    for param, value in serialized_params.items():
        memory_flags.append(f"--{param}={value}")

    try:
        output, results = run_sysbench(params, memory_flags, "memory")
    except Exception as error:
        return "error", WorkloadError(error.args[0], error.args[1])

    print("==>> Workload run complete!")

    return "success", WorkloadResultsMemory(
        sysbench_memory_output_schema.unserialize(output),
        sysbench_memory_results_schema.unserialize(results),
    )


if __name__ == "__main__":
    sys.exit(
        plugin.run(plugin.build_schema(RunSysbenchCpu, RunSysbenchMemory))
    )

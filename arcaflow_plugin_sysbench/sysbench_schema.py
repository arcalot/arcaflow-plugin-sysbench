import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin


@dataclass
class CommonInputParameters:
    operation: str = field(
        metadata={
            "name": "Operation",
            "description": "Sysbench Operation to perform",
        }
    )
    threads: typing.Optional[int] = field(
        default=1,
        metadata={
            "name": "Threads",
            "description": "Number of worker threads to create",
        },
    )
    events: typing.Optional[int] = field(
        default=0,
        metadata={
            "name": "Number of events",
            "description": "Maximum number of events",
        },
    )
    time: typing.Optional[int] = field(
        default=10,
        metadata={
            "name": "Time",
            "description": "Limit for total execution time in seconds",
        },
    )


@dataclass
class SysbenchCpuInputParams(CommonInputParameters):
    """
    This is the data structure for the
    input parameters of Sysbench CPU benchmark.
    """

    cpumaxprime: typing.Optional[int] = field(
        default=10000,
        metadata={
            "name": "CPU max prime",
            "description": (
                "The upper limit of the number of prime numbers generated"
            ),
        },
    )


@dataclass
class SysbenchMemoryInputParams(CommonInputParameters):
    """
    This is the data structure for the
    input parameters of Sysbench Memory benchmark.
    """

    memoryblocksize: typing.Optional[str] = field(
        default="1KiB",
        metadata={
            "name": "Block Size",
            "description": "size of memory block for test in KiB/MiB/GiB",
        },
    )
    memorytotalsize: typing.Optional[str] = field(
        default="100G",
        metadata={
            "name": "Total Size",
            "description": "Total size of data to transfer in GiB",
        },
    )
    memoryscope: typing.Optional[str] = field(
        default="global",
        metadata={
            "name": "Memory Scope",
            "description": "Memory Access Scope(global/local)",
        },
    )
    memoryoperation: typing.Optional[str] = field(
        default="write",
        metadata={
            "name": "Memory Operation",
            "description": "Type of memory operation(write/read)",
        },
    )


@dataclass
class LatencyAggregates:
    avg: float = field(
        metadata={"name": "Average", "description": "Average Latency"}
    )
    min: float = field(
        metadata={"name": "Minimum", "description": "Minimum latency"}
    )
    max: float = field(
        metadata={"name": "Maximum", "description": "Maximum Latency"}
    )
    P95thpercentile: float = field(
        metadata={
            "name": "95th Percentile",
            "description": "95th percentile latency",
        }
    )
    sum: float = field(
        metadata={"name": "Sum", "description": "Sum of latencies"}
    )


@dataclass
class ThreadFairnessAggregates:
    avg: float = field(
        metadata={
            "name": "Average",
            "description": "Average value across all threads",
        }
    )
    stddev: float = field(
        metadata={
            "name": "Standard Deviation",
            "description": "Standard deviation of all threads",
        }
    )


@dataclass
class ThreadsFairness:
    events: ThreadFairnessAggregates = field(
        metadata={
            "name": "Thread Fairness events",
            "description": "number of events executed by the threads ",
        }
    )
    executiontime: ThreadFairnessAggregates = field(
        metadata={
            "name": "Thread Fairness execution time",
            "description": "Execution time of threads",
        }
    )


@dataclass
class CPUmetrics:
    eventspersecond: float = field(
        metadata={
            "name": "Events per second",
            "description": "Number of events per second to measure CPU speed",
        }
    )


@dataclass
class SysbenchMemoryOutputParams:
    """
    This is the data structure for output
    parameters returned by sysbench memory benchmark.
    """

    totaltime: float = field(
        metadata={
            "name": "Total time",
            "description": "Total execution time of workload",
        }
    )
    totalnumberofevents: float = field(
        metadata={
            "name": "Total number of events",
            "description": "Total number of events performed by the workload",
        }
    )
    blocksize: str = field(
        metadata={"name": "Block size", "description": "Block size in KiB"}
    )
    totalsize: str = field(
        metadata={"name": "Total size", "description": "Total size in MiB"}
    )
    operation: str = field(
        metadata={
            "name": "Operation",
            "description": "memory operation performed",
        }
    )
    scope: str = field(
        metadata={"name": "Scope", "description": "scope of operation"}
    )
    Totaloperationspersecond: float = field(
        metadata={
            "name": "Total operations per second",
            "description": (
                "Total number of operations performed by the memory workload"
                " per second"
            ),
        }
    )
    Totaloperations: float = field(
        metadata={
            "name": "Total operations",
            "description": (
                "Total number of operations performed by the memory workload"
            ),
        }
    )
    Numberofthreads: float = field(
        metadata={
            "name": "Number of threads",
            "description": "Number of threads used by the workload",
        }
    )


@dataclass
class SysbenchCpuOutputParams:
    """
    This is the data structure for output
    parameters returned by sysbench cpu benchmark.
    """

    totaltime: float = field(
        metadata={
            "name": "Total time",
            "description": "Total execution time of workload",
        }
    )
    totalnumberofevents: float = field(
        metadata={
            "name": "Total number of events",
            "description": "Total number of events performed by the workload",
        }
    )
    Primenumberslimit: float = field(
        metadata={
            "name": "Prime numbers limit",
            "description": "Number of prime numbers to use for CPU workload",
        }
    )
    Numberofthreads: float = field(
        metadata={
            "name": "Number of threads",
            "description": "Number of threads used by the workload",
        }
    )


@dataclass
class SysbenchMemoryResultParams:
    """
    This is the output results data structure for sysbench memory results.
    """

    transferred_MiB: float = field(
        metadata={
            "name": "Transferred memory",
            "description": "Total Memory Transferred",
        }
    )
    transferred_MiBpersec: float = field(
        metadata={
            "name": "Transferred memory per second",
            "description": "Total Memory Transferred per second",
        }
    )
    Latency: LatencyAggregates = field(
        metadata={
            "name": "Latency",
            "description": "Memory Latency in mili seconds",
        }
    )
    Threadsfairness: ThreadsFairness = field(
        metadata={
            "name": "Threads fairness",
            "description": (
                "Event distribution by threads for number of executed events"
                " by threads and total execution time by thread"
            ),
        }
    )


@dataclass
class SysbenchCpuResultParams:
    """
    This is the output results data structure for sysbench cpu results.
    """

    CPUspeed: CPUmetrics = field(
        metadata={
            "name": "CPU speed",
            "description": "No of events per second",
        }
    )
    Latency: LatencyAggregates = field(
        metadata={
            "name": "Latency",
            "description": "CPU latency in miliseconds",
        }
    )
    Threadsfairness: ThreadsFairness = field(
        metadata={
            "name": "Threads fairness",
            "description": (
                "Event distribution by threads for number of executed events"
                " by threads and total execution time by thread"
            ),
        }
    )


@dataclass
class WorkloadResultsCpu:
    """
    This is the output results data structure
    for the Sysbench CPU success case.
    """

    sysbench_output_params: SysbenchCpuOutputParams = field(
        metadata={
            "name": "Sysbench Cpu Output Parameters",
            "description": (
                "Ouptut parameters for a successful sysbench cpu workload"
                " execution"
            ),
        }
    )
    sysbench_results: SysbenchCpuResultParams = field(
        metadata={
            "name": "Sysbench Cpu Result Parameters",
            "description": (
                "Result parameters for a successful sysbench cpu workload"
                " execution"
            ),
        }
    )


@dataclass
class WorkloadResultsMemory:
    """
    This is the output results data structure
    for the Sysbench memory success case.
    """

    sysbench_output_params: SysbenchMemoryOutputParams = field(
        metadata={
            "name": "Sysbench Memory Output Parameters",
            "description": (
                "Ouptut parameters for a successful sysbench memory workload"
                " execution"
            ),
        }
    )
    sysbench_results: SysbenchMemoryResultParams = field(
        metadata={
            "name": "Sysbench Memory Result Parameters",
            "description": (
                "Result parameters for a successful sysbench Memory workload"
                " execution"
            ),
        }
    )


@dataclass
class WorkloadError:
    """
    This is the output data structure in the error case.
    """

    exit_code: int = field(
        metadata={
            "name": "Exit Code",
            "description": (
                "Exit code returned by the program in case of a failure"
            ),
        }
    )
    error: str = field(
        metadata={"name": "Failure Error", "description": "Reason for failure"}
    )

sysbench_cpu_output_schema = plugin.build_object_schema(
    SysbenchCpuOutputParams
)
sysbench_cpu_results_schema = plugin.build_object_schema(
    SysbenchCpuResultParams
)
sysbench_memory_output_schema = plugin.build_object_schema(
    SysbenchMemoryOutputParams
)
sysbench_memory_results_schema = plugin.build_object_schema(
    SysbenchMemoryResultParams
)

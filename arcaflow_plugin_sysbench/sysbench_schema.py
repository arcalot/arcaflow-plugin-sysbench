import typing
from dataclasses import dataclass
from arcaflow_plugin_sdk import plugin, schema


@dataclass
class CommonInputParameters:
    threads: typing.Annotated[
        typing.Optional[int],
        schema.name("Threads"),
        schema.description("Number of worker threads to create"),
    ] = 1
    events: typing.Annotated[
        typing.Optional[int],
        schema.name("Number of events"),
        schema.description("Maximum number of events"),
    ] = 9
    time: typing.Annotated[
        typing.Optional[int],
        schema.name("Time"),
        schema.description("Limit for total execution time in seconds"),
    ] = 10


@dataclass
class SysbenchCpuInputParams(CommonInputParameters):
    """
    This is the data structure for the
    input parameters of Sysbench CPU benchmark.
    """

    cpumaxprime: typing.Annotated[
        typing.Optional[int],
        schema.name("CPU max prime"),
        schema.description(
            "The upper limit of the number of prime numbers generated"
        ),
    ] = 10000


@dataclass
class SysbenchMemoryInputParams(CommonInputParameters):
    """
    This is the data structure for the
    input parameters of Sysbench Memory benchmark.
    """

    memoryblocksize: typing.Annotated[
        typing.Optional[str],
        schema.name("Block Size"),
        schema.description("size of memory block for test in KiB/MiB/GiB"),
    ] = "1KiB"
    memorytotalsize: typing.Annotated[
        typing.Optional[str],
        schema.name("Total Size"),
        schema.description("Total size of data to transfer in GiB"),
    ] = "100G"
    memoryscope: typing.Annotated[
        typing.Optional[str],
        schema.name("Memory Scope"),
        schema.description("Memory Access Scope(global/local)"),
    ] = "global"
    memoryoperation: typing.Annotated[
        typing.Optional[str],
        schema.name("Memory Operation"),
        schema.description("Type of memory operation(write/read)"),
    ] = "write"


@dataclass
class LatencyAggregates:
    avg: typing.Annotated[
        float,
        schema.name("Average"),
        schema.description("Average Latency"),
    ]
    min: typing.Annotated[
        float,
        schema.name("Minimum"),
        schema.description("Minimum latency"),
    ]
    max: typing.Annotated[
        float,
        schema.name("Maximum"),
        schema.description("Maximum Latency"),
    ]
    P95thpercentile: typing.Annotated[
        float,
        schema.name("95th Percentile"),
        schema.description("95th percentile latency"),
    ]
    sum: typing.Annotated[
        float,
        schema.name("Sum"),
        schema.description("Sum of latencies"),
    ]


@dataclass
class ThreadFairnessAggregates:
    avg: typing.Annotated[
        float,
        schema.name("Average"),
        schema.description("Average value across all threads"),
    ]
    stddev: typing.Annotated[
        float,
        schema.name("Standard Deviation"),
        schema.description("Standard deviation of all threads"),
    ]


@dataclass
class ThreadsFairness:
    events: typing.Annotated[
        ThreadFairnessAggregates,
        schema.name("Thread Fairness events"),
        schema.description("number of events executed by the threads "),
    ]
    executiontime: typing.Annotated[
        ThreadFairnessAggregates,
        schema.name("Thread Fairness execution time"),
        schema.description("Execution time of threads"),
    ]


@dataclass
class CPUmetrics:
    eventspersecond: typing.Annotated[
        float,
        schema.name("Events per second"),
        schema.description("Number of events per second to measure CPU speed"),
    ]


@dataclass
class SysbenchMemoryOutputParams:
    """
    This is the data structure for output
    parameters returned by sysbench memory benchmark.
    """

    totaltime: typing.Annotated[
        float,
        schema.name("Total time"),
        schema.description("Total execution time of workload"),
    ]
    totalnumberofevents: typing.Annotated[
        float,
        schema.name("Total number of events"),
        schema.description("Total number of events performed by the workload"),
    ]
    blocksize: typing.Annotated[
        str,
        schema.name("Block size"),
        schema.description("Block size in KiB"),
    ]
    totalsize: typing.Annotated[
        str,
        schema.name("Total size"),
        schema.description("Total size in MiB"),
    ]
    operation: typing.Annotated[
        str,
        schema.name("Operation"),
        schema.description("memory operation performed"),
    ]
    scope: typing.Annotated[
        str,
        schema.name("Scope"),
        schema.description("scope of operation"),
    ]
    Totaloperationspersecond: typing.Annotated[
        float,
        schema.name("Total operations per second"),
        schema.description(
            "Total number of operations performed by the memory workload"
            " per second"
        ),
    ]
    Totaloperations: typing.Annotated[
        float,
        schema.name("Total operations"),
        schema.description(
            "Total number of operations performed by the memory workload"
        ),
    ]
    Numberofthreads: typing.Annotated[
        float,
        schema.name("Number of threads"),
        schema.description("Number of threads used by the workload"),
    ]


@dataclass
class SysbenchCpuOutputParams:
    """
    This is the data structure for output
    parameters returned by sysbench cpu benchmark.
    """

    totaltime: typing.Annotated[
        float,
        schema.name("Total time"),
        schema.description("Total execution time of workload"),
    ]
    totalnumberofevents: typing.Annotated[
        float,
        schema.name("Total number of events"),
        schema.description("Total number of events performed by the workload"),
    ]
    Primenumberslimit: typing.Annotated[
        float,
        schema.name("Prime numbers limit"),
        schema.description("Number of prime numbers to use for CPU workload"),
    ]
    Numberofthreads: typing.Annotated[
        float,
        schema.name("Number of threads"),
        schema.description("Number of threads used by the workload"),
    ]


@dataclass
class SysbenchMemoryResultParams:
    """
    This is the output results data structure for sysbench memory results.
    """

    transferred_MiB: typing.Annotated[
        float,
        schema.name("Transferred memory"),
        schema.description("Total Memory Transferred"),
    ]
    transferred_MiBpersec: typing.Annotated[
        float,
        schema.name("Transferred memory per second"),
        schema.description("Total Memory Transferred per second"),
    ]
    Latency: typing.Annotated[
        LatencyAggregates,
        schema.name("Latency"),
        schema.description("Memory Latency in mili seconds"),
    ]
    Threadsfairness: typing.Annotated[
        ThreadsFairness,
        schema.name("Threads fairness"),
        schema.description(
            "Event distribution by threads for number of executed events"
            " by threads and total execution time by thread"
        ),
    ]


@dataclass
class SysbenchCpuResultParams:
    """
    This is the output results data structure for sysbench cpu results.
    """

    CPUspeed: typing.Annotated[
        CPUmetrics,
        schema.name("CPU speed"),
        schema.description("No of events per second"),
    ]
    Latency: typing.Annotated[
        LatencyAggregates,
        schema.name("Latency"),
        schema.description("CPU latency in miliseconds"),
    ]
    Threadsfairness: typing.Annotated[
        ThreadsFairness,
        schema.name("Threads fairness"),
        schema.description(
            "Event distribution by threads for number of executed events"
            " by threads and total execution time by thread"
        ),
    ]


@dataclass
class WorkloadResultsCpu:
    """
    This is the output results data structure
    for the Sysbench CPU success case.
    """

    sysbench_output_params: typing.Annotated[
        SysbenchCpuOutputParams,
        schema.name("Sysbench Cpu Output Parameters"),
        schema.description(
            "Ouptut parameters for a successful sysbench cpu workload"
            " execution"
        ),
    ]
    sysbench_results: typing.Annotated[
        SysbenchCpuResultParams,
        schema.name("Sysbench Cpu Result Parameters"),
        schema.description(
            "Result parameters for a successful sysbench cpu workload"
            " execution"
        ),
    ]


@dataclass
class WorkloadResultsMemory:
    """
    This is the output results data structure
    for the Sysbench memory success case.
    """

    sysbench_output_params: typing.Annotated[
        SysbenchMemoryOutputParams,
        schema.name("Sysbench Memory Output Parameters"),
        schema.description(
            "Ouptut parameters for a successful sysbench memory workload"
            " execution"
        ),
    ]
    sysbench_results: typing.Annotated[
        SysbenchMemoryResultParams,
        schema.name("Sysbench Memory Result Parameters"),
        schema.description(
            "Result parameters for a successful sysbench Memory workload"
            " execution"
        ),
    ]


@dataclass
class WorkloadError:
    """
    This is the output data structure in the error case.
    """

    exit_code: typing.Annotated[
        int,
        schema.name("Exit Code"),
        schema.description(
            "Exit code returned by the program in case of a failure"
        ),
    ]
    error: typing.Annotated[
        str,
        schema.name("Failure Error"),
        schema.description("Reason for failure"),
    ]


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

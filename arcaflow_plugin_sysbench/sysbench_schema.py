import enum
import typing
from dataclasses import dataclass
from arcaflow_plugin_sdk import plugin, schema, validation


class OnOff(enum.Enum):
    ON = "on"
    OFF = "off"


class RandType(enum.Enum):
    UNIFORM = "uniform"
    GAUSSIAN = "gaussian"
    SPECIAL = "special"
    PARETO = "pareto"


class SeqRnd(enum.Enum):
    SEQ = "seq"
    RND = "rnd"


class GlobalLocal(enum.Enum):
    GLOBAL = "global"
    LOCAL = "local"


class RWN(enum.Enum):
    READ = "read"
    WRITE = "write"
    NONE = "none"


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
    forced_shutdown: typing.Annotated[
        typing.Optional[int],
        schema.id("forced-shutdown"),
        schema.name("Forced Shutdown Seconds"),
        schema.description(
            "Number of seconds to wait after the 'time' limit before forcing"
            " shutdown, or exclude parameter to disable forced shutdown"
        ),
    ] = None
    thread_stack_size: typing.Annotated[
        typing.Optional[str],
        schema.id("thread-stack-size"),
        schema.name("Thread stack size"),
        schema.description("size of stack per thread"),
    ] = "64K"
    rate: typing.Annotated[
        typing.Optional[int],
        schema.name("Transaction rate"),
        schema.description("average transactions rate. 0 for unlimited rate"),
    ] = 0
    validate: typing.Annotated[
        typing.Optional[OnOff],
        schema.name("Validate"),
        schema.description("perform validation checks where possible"),
    ] = OnOff.OFF
    rand_type: typing.Annotated[
        typing.Optional[RandType],
        schema.id("rand-type"),
        schema.name("Random Number Type"),
        schema.description("Random numbers distribution"),
    ] = RandType.SPECIAL
    rand_spec_iter: typing.Annotated[
        typing.Optional[int],
        schema.id("rand-spec-iter"),
        schema.name("Rand spec iterations"),
        schema.description("Number of iterations used for numbers generation"),
    ] = 12
    rand_spec_pct: typing.Annotated[
        typing.Optional[int],
        schema.id("rand-spec-pct"),
        schema.name("Rand spec percentage"),
        schema.description(
            "Percentage of values to be treated as 'special' (for special"
            " distribution)"
        ),
    ] = 1
    rand_spec_res: typing.Annotated[
        typing.Optional[int],
        schema.id("rand-spec-res"),
        schema.name("Rand spec res"),
        schema.description(
            "Percentage of 'special' values to use (for special distribution)"
        ),
    ] = 75
    rand_seed: typing.Annotated[
        typing.Optional[int],
        schema.id("rand-seed"),
        schema.name("Rand seed"),
        schema.description(
            "seed for random number generator. When 0, the current time is"
            " used as a RNG seed."
        ),
    ] = 0
    rand_pareto_h: typing.Annotated[
        typing.Optional[float],
        schema.id("rand-pareto-h"),
        schema.name("Rand pareto h"),
        schema.description("parameter h for pareto distribution"),
    ] = 0.2
    percentile: typing.Annotated[
        typing.Optional[int],
        validation.min(0),
        validation.max(100),
        schema.name("Percentile"),
        schema.description(
            "percentile to calculate in latency statistics (1-100)."
            " Use the special value of 0 to disable percentile calculations"
        ),
    ] = 95


# Other common parameters to consider...

# Implementing report-interval would add periodic output to stdout and a new
# data format we would need to account for in the parse_output section
# of the plugin
#   --report-interval=N             periodically report intermediate
# statistics with a specified interval in seconds. 0 disables intermediate
# reports [0]

# Implementing report-checkpoints would dump to stdout a full run output at
# the checkpoint times, requiring additional processing in the parse_output
# section of the plugin
#   --report-checkpoints=[LIST,...] dump full statistics and reset all
# counters at specified points in time. The argument is a list of
# comma-separated values representing the amount of time in seconds elapsed
# from start of test when report checkpoint(s) must be performed. Report
# checkpoints are off by default. []

# Implementing debug would add more verbose output ot stdout that we would
# need to adjust parse_output to process.
#   --debug[=on|off]                print more debugging info [off]

# Implementing verbosity changes the output and would require adjustments to
# the parse_output process.
#   --verbosity=N verbosity level {5 - debug, 0 - only critical messages} [3]

# Implementing histogram significantly adds to the output, but this might be
# valuable information to capture, even by default.
#   --histogram[=on|off] print latency histogram in report [off]


@dataclass
class SysbenchCpuInputParams(CommonInputParameters):
    """
    This is the data structure for the
    input parameters of Sysbench CPU benchmark.
    """

    cpu_max_prime: typing.Annotated[
        typing.Optional[int],
        schema.id("cpu-max-prime"),
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

    memory_block_size: typing.Annotated[
        typing.Optional[str],
        schema.id("memory-block-size"),
        schema.name("Block Size"),
        schema.description("size of memory block for test in KiB/MiB/GiB"),
    ] = "1KiB"
    memory_total_size: typing.Annotated[
        typing.Optional[str],
        schema.id("memory-total-size"),
        schema.name("Total Size"),
        schema.description("Total size of data to transfer in GiB"),
    ] = "100G"
    memory_scope: typing.Annotated[
        typing.Optional[GlobalLocal],
        schema.id("memory-scope"),
        schema.name("Memory Scope"),
        schema.description("Memory Access Scope(global/local)"),
    ] = GlobalLocal.GLOBAL
    memory_oper: typing.Annotated[
        typing.Optional[RWN],
        schema.id("memory-oper"),
        schema.name("Memory Operation"),
        schema.description("Type of memory operation(write/read)"),
    ] = RWN.WRITE
    memory_hugetlb: typing.Annotated[
        typing.Optional[OnOff],
        schema.id("memory-hugetlb"),
        schema.name("Memory hugetlb"),
        schema.description("Allocate memory from HugeTLB pool (on/off)"),
    ] = OnOff.OFF
    memory_access_mode: typing.Annotated[
        typing.Optional[SeqRnd],
        schema.id("memory-access-mode"),
        schema.name("Memory Access Mode"),
        schema.description("memory access mode (seq,rnd)"),
    ] = SeqRnd.SEQ


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
class SysbenchCommonOutputParams:
    """
    This is the data structure for common output
    parameters returned by sysbench benchmarks.
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
    Numberofthreads: typing.Annotated[
        float,
        schema.name("Number of threads"),
        schema.description("Number of threads used by the workload"),
    ]
    Validationchecks: typing.Annotated[
        typing.Optional[str],
        schema.name("Validation checks"),
        schema.description("Validation on/off"),
    ] = "off"


@dataclass
class SysbenchMemoryOutput:
    """
    This is the data structure for specific output
    parameters returned by sysbench memory benchmark.
    """

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


@dataclass
class SysbenchCpuOutput:
    """
    This is the data structure for specific output
    parameters returned by sysbench cpu benchmark.
    """

    Primenumberslimit: typing.Annotated[
        float,
        schema.name("Prime numbers limit"),
        schema.description("Number of prime numbers to use for CPU workload"),
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
class SysbenchMemoryOutputParams(SysbenchCommonOutputParams,SysbenchMemoryOutput):
    """
    This is the data structure for all output
    parameters returned by sysbench memory benchmark.
    """

@dataclass
class SysbenchCpuOutputParams(SysbenchCommonOutputParams,SysbenchCpuOutput):
    """
    This is the data structure for all output
    parameters returned by sysbench cpu benchmark.
    """

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


sysbench_cpu_input_schema = plugin.build_object_schema(SysbenchCpuInputParams)
sysbench_memory_input_schema = plugin.build_object_schema(
    SysbenchMemoryInputParams
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

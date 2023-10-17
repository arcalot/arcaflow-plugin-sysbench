#!/usr/bin/env python3

import unittest
import sysbench_plugin
from arcaflow_plugin_sdk import plugin

import sysbench_schema


class SysbenchPluginTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            sysbench_plugin.SysbenchCpuInputParams(threads=2)
        )

        plugin.test_object_serialization(
            sysbench_plugin.SysbenchMemoryInputParams(threads=2)
        )
        plugin.test_object_serialization(
            sysbench_plugin.sysbench_cpu_output_schema.unserialize(
                {
                    "Numberofthreads": 2,
                    "Primenumberslimit": 10000,
                    "totaltime": 10.0008,
                    "totalnumberofevents": 26401.0,
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.sysbench_cpu_results_schema.unserialize(
                {
                    "CPUspeed": {"eventspersecond": "2639.51"},
                    "Latency": {
                        "min": "0.67",
                        "avg": "0.76",
                        "max": "1.26",
                        "percentile": 95,
                        "percentile_value": "1.25",
                        "sum": "19987.57",
                    },
                    "Threadsfairness": {
                        "events": {"avg": 13200.5, "stddev": 17.5},
                        "executiontime": {"avg": 9.9938, "stddev": 0.0},
                    },
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.sysbench_memory_output_schema.unserialize(
                {
                    "Numberofthreads": 2,
                    "blocksize": "1KiB",
                    "totalsize": "102400MiB",
                    "operation": "write",
                    "scope": "global",
                    "Totaloperations": 72227995.0,
                    "Totaloperationspersecond": 7221925.38,
                    "totaltime": 10.0001,
                    "totalnumberofevents": 72227995.0,
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.sysbench_memory_results_schema.unserialize(
                {
                    "transferred_MiB": 70535.15,
                    "transferred_MiBpersec": 7052.66,
                    "Latency": {
                        "min": "0.00",
                        "avg": "0.00",
                        "max": "1.18",
                        "percentile": 95,
                        "percentile_value": "1.17",
                        "sum": "13699.95",
                    },
                    "Threadsfairness": {
                        "events": {"avg": 36113997.5, "stddev": 710393.5},
                        "executiontime": {"avg": 6.85, "stddev": 0.07},
                    },
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.sysbench_io_output_schema.unserialize(
                {
                    "Numberofthreads": 2,
                    "NumberofIOrequests": 0,
                    "ReadWriteratioforcombinedrandomIOtest": 0,
                    "Extrafileopenflags": "sync",
                    "totaltime": 0.0114,
                    "totalnumberofevents": 9.0,
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.sysbench_io_results_schema.unserialize(
                {
                    "Fileoperations": {
                        "reads_s": "0.00",
                        "writes_s": "689.64",
                        "fsyncs_s": "306.50",
                    },
                    "Throughput": {
                        "read_MiB_s": "0.00",
                        "written_MiB_s": "10.78",
                    },
                    "Latency": {
                        "min": "1.53",
                        "avg": "2.31",
                        "max": "4.08",
                        "percentile": 95,
                        "percentile_value": "4.07",
                        "sum": "20.75",
                    },
                    "Threadsfairness": {
                        "events": {"avg": 4.5, "stddev": 0.5},
                        "executiontime": {"avg": 0.0104, "stddev": 0.0},
                    },
                }
            )
        )

        plugin.test_object_serialization(
            sysbench_plugin.WorkloadError(exit_code=1, error="This is an error")
        )

    def test_functional_cpu(self):
        input = sysbench_plugin.SysbenchCpuInputParams(threads=2)

        output_id, output_data = sysbench_plugin.RunSysbenchCpu(input)

        self.assertEqual("success", output_id)
        self.assertGreaterEqual(output_data.sysbench_output_params.Numberofthreads, 1)
        self.assertGreater(output_data.sysbench_output_params.totaltime, 0)
        self.assertGreater(output_data.sysbench_output_params.totalnumberofevents, 0)
        self.assertGreater(output_data.sysbench_results.CPUspeed.eventspersecond, 0)
        self.assertGreaterEqual(output_data.sysbench_results.Latency.avg, 0)
        self.assertGreaterEqual(output_data.sysbench_results.Latency.sum, 0)
        self.assertGreater(output_data.sysbench_results.Threadsfairness.events.avg, 0)
        self.assertGreater(
            output_data.sysbench_results.Threadsfairness.executiontime.avg, 0
        )

    def test_functional_memory(self):
        input = sysbench_plugin.SysbenchMemoryInputParams(threads=2)

        output_id, output_data = sysbench_plugin.RunSysbenchMemory(input)

        self.assertEqual("success", output_id)
        self.assertGreaterEqual(output_data.sysbench_output_params.Numberofthreads, 1)
        self.assertGreater(output_data.sysbench_output_params.totaltime, 0)
        self.assertGreater(output_data.sysbench_output_params.Totaloperations, 0)
        self.assertIsNotNone(output_data.sysbench_output_params.blocksize)
        self.assertIsNotNone(output_data.sysbench_output_params.operation)
        self.assertGreater(output_data.sysbench_results.transferred_MiB, 0)
        self.assertGreater(output_data.sysbench_results.transferred_MiBpersec, 0)
        self.assertGreaterEqual(output_data.sysbench_results.Latency.avg, 0)
        self.assertGreaterEqual(output_data.sysbench_results.Latency.sum, 0)
        self.assertGreater(output_data.sysbench_results.Threadsfairness.events.avg, 0)
        self.assertGreater(
            output_data.sysbench_results.Threadsfairness.executiontime.avg, 0
        )

    def test_functional_io(self):
        input = sysbench_plugin.SysbenchIoInputParams(
            events=0,
            threads=2,
            file_num=2,
            file_total_size="12M",
            file_extra_flags=sysbench_schema.FileExtraFlag.SYNC,
            file_fsync_freq=100,
            file_fsync_all=sysbench_schema.OnOff.OFF,
            file_fsync_end=sysbench_schema.OnOff.ON,
            file_fsync_mode=sysbench_schema.FileSyncMode.FSYNC,
            file_test_mode=sysbench_schema.FileTestMode.RNDRW,
            time=10,
        )
        output_id, output_data = sysbench_plugin.RunSysbenchIo(input)

        self.assertEqual("success", output_id)
        self.assertEqual(output_data.sysbench_output_params.Numberofthreads, 2)
        self.assertGreaterEqual(output_data.sysbench_output_params.totaltime, 10)
        self.assertGreater(output_data.sysbench_output_params.totalnumberofevents, 0)
        self.assertGreater(
            output_data.sysbench_output_params.ReadWriteratioforcombinedrandomIOtest,
            0.0,
        )
        self.assertGreater(output_data.sysbench_results.Fileoperations.reads_s, 0)
        self.assertGreater(output_data.sysbench_results.Fileoperations.writes_s, 0)
        self.assertGreater(output_data.sysbench_results.Fileoperations.fsyncs_s, 0)
        self.assertGreater(output_data.sysbench_results.Throughput.read_MiB_s, 0)
        self.assertGreater(output_data.sysbench_results.Throughput.written_MiB_s, 0)
        self.assertGreaterEqual(output_data.sysbench_results.Latency.min, 0)
        self.assertGreater(output_data.sysbench_results.Latency.avg, 0)
        self.assertGreater(output_data.sysbench_results.Latency.max, 0)
        self.assertGreater(output_data.sysbench_results.Latency.percentile, 0)
        self.assertGreater(output_data.sysbench_results.Latency.sum, 0)
        self.assertGreater(output_data.sysbench_results.Threadsfairness.events.avg, 0)
        self.assertGreater(output_data.sysbench_results.Threadsfairness.events.avg, 0)
        self.assertGreater(
            output_data.sysbench_results.Threadsfairness.executiontime.avg, 0
        )

    def test_parsing_function_memory(self):
        sysbench_output = {
            "Numberofthreads": 2,
            "blocksize": "1KiB",
            "totalsize": "102400MiB",
            "operation": "write",
            "scope": "global",
            "Totaloperations": 70040643.0,
            "Totaloperationspersecond": 7003215.47,
            "totaltime": 10.0001,
            "totalnumberofevents": 70040643.0,
        }
        sysbench_results = {
            "transferred_MiB": 68399.07,
            "transferred_MiBpersec": 6839.08,
            "Latency": {
                "min": "0.00",
                "avg": "0.00",
                "max": "0.11",
                "percentile": 95,
                "percentile_value": "0.00",
                "sum": "13958.52",
            },
            "Threadsfairness": {
                "events": {"avg": 35020321.5, "stddev": 955973.5},
                "executiontime": {"avg": 6.9793, "stddev": 0.07},
            },
        }
        with open("tests/memory_parse_output.txt", "r") as fout:
            mem_output = fout.read()

        output, results = sysbench_plugin.parse_output(mem_output)
        self.assertEqual(sysbench_output, output)
        self.assertEqual(sysbench_results, results)

    def test_parsing_function_cpu(self):
        sysbench_output = {
            "Numberofthreads": 2,
            "Primenumberslimit": 10000,
            "totaltime": 10.0005,
            "totalnumberofevents": 29281.0,
        }
        sysbench_results = {
            "CPUspeed": {"eventspersecond": "2927.61"},
            "Latency": {
                "min": "0.67",
                "avg": "0.68",
                "max": "1.56",
                "percentile": 95,
                "percentile_value": "0.70",
                "sum": "19995.74",
            },
            "Threadsfairness": {
                "events": {"avg": 14640.5, "stddev": 1.5},
                "executiontime": {"avg": 9.9979, "stddev": 0.0},
            },
        }

        with open("tests/cpu_parse_output.txt", "r") as fout:
            cpu_output = fout.read()

        output, results = sysbench_plugin.parse_output(cpu_output)
        self.assertEqual(sysbench_output, output)
        self.assertEqual(sysbench_results, results)

    def test_parsing_function_io(self):
        sysbench_output = {
            "Numberofthreads": 2,
            "Extrafileopenflags": "sync",
            "totaltime": 60.0028,
            "totalnumberofevents": 36776.0,
        }

        sysbench_results = {
            "Fileoperations": {
                "reads_s": "0.00",
                "writes_s": "600.89",
                "fsyncs_s": "12.07",
            },
            "Throughput": {"read_MiB_s": "0.00", "written_MiB_s": "9.39"},
            "Latency": {
                "min": "0.10",
                "avg": "3.26",
                "max": "43.90",
                "percentile": 95,
                "percentile_value": "5.09",
                "sum": "119963.98",
            },
            "Threadsfairness": {
                "events": {"avg": 18388.0, "stddev": 10.0},
                "executiontime": {"avg": 59.982, "stddev": 0.0},
            },
        }
        with open("tests/io_parse_output.txt", "r") as fout:
            cpu_output = fout.read()

        output, results = sysbench_plugin.parse_output(cpu_output)
        self.assertEqual(sysbench_output, output)
        self.assertEqual(sysbench_results, results)


if __name__ == "__main__":
    unittest.main()

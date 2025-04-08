# Kueuer Benchmarking Toolkit

Kueuer is a python package for benchmarking the performance and behavior of the deploying containerized workloads on a Kubernetes cluster. It provides a command line interface (CLI) for launching benchmarks, running jobs, and plotting results.

## Installation

To install Kueuer, you can use pip:

```bash
git clone https://github.com/opencadc/deployments.git
cd deployments/configs/kueue/kueuer
pip install -e .
```

Alternatively, it is also highly reccommended to install and run Kueuer in a virtual environment to avoid any conflicts with other packages.
Provided below is an example to do this, using the tool `uv`;

```bash
# Install uv
pip3 --user install uv
cd deployments/configs/kueue/kueuer
uv sync
uv run kr --help
```

## Goals

The goal of Kueuer is to provide a simple and efficient way to benchmark the performance of Kubernetes job scheduling and eviction behavior against Kubernetes Kueue. It is designed to for cluster administrators and developers who want to test the performance of their Kubernetes clusters and workloads, and iterate on their configurations.

## Features
- *Benchmarks*: Kueuer provides benchamrks to test the performance of Kubernetes job scheduling and eviction behavior.
- *Jobs*: Kueuer provides a simple interface to launch and delete massive number of jobs on a Kubernetes cluster to simulate stress.
- *Plots*: For performance benchmarks, Kueuer provides a simple interface for generating plots from results.

## Cluster Requirements
- Kubernetes cluster with Kueue installed. See the [Kueue documentation](https://kueue.sigs.k8s.io).
- Kueue configuration used by CADC can be found under [opencadc/deployments/configs/kueue](https://github.com/opencadc/deployments/configs/kueue/README.md)
- Kubernetes cluster access to create and delete jobs, and to install Kueue.


## Benchmarks

Kueuer provides benchmarking to evaluate the performance of Kubernetes job scheduling and eviction behavior. The benchmarks are designed to compare native Kubernetes job scheduling with the advanced capabilities of Kubernetes Kueue. This allows users to assess the impact of Kueue on job throughput, latency, and resource utilization. The default job configuration is set to use 1 CPU core, 1 GB of RAM, and 1 GB of ephemeral storage. The benchmarks can be customized to test different job configurations varying CPU, RAM, and storage requirements through the CLI. If you wish to change the default job configuration outside of the options provided, you can modify the job template file located at `src/kueuer/benchmarks/job.yaml`. The job template is a standard Kubernetes job specification and can be customized to suit your needs.

### Benchmark Types

1. **Performance Benchmarks**:
   - Compare the scheduling efficiency and job execution times between native Kubernetes and Kueue.
   - Measure metrics such as throughput, startup latency, completion latency, and coefficient of variation, etc.
   - Generate comparative improvement metrics to evaluate the benefits of using Kueue.

2. **Eviction Benchmarks**:
   - Test the eviction behavior of Kueue in a packed cluster queue.
   - Analyze priority rule violations during preemptions and ensure workloads with higher priorities are not evicted by lower-priority workloads.

### Running Benchmarks

To run benchmarks, use the `kr benchmark` command. This command provides two subcommands:

#### Performance Benchmarks

The performance benchmark launches a series of jobs with increasing job counts, starting from 2^1 to 2^N. The benchmark tails the Kubernetes API server to capture the job scheduling and completion events and generates a CSV file with the results. 

[![asciicast](https://asciinema.org/a/WsSGGVuyLRHTxzzUbcI3XR5rh.svg)](https://asciinema.org/a/WsSGGVuyLRHTxzzUbcI3XR5rh)

| Option             | Shorthand | Type    | Description                                                                                     | Default                                                                                     |
|--------------------|-----------|---------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `--filepath`       | `-f`      | TEXT    | K8s job template.                                                                              | `/src/kueuer/benchmarks/job.yaml` |
| `--namespace`      | `-n`      | TEXT    | Namespace to launch jobs in.                                                                   | `skaha-workload`                                                                            |
| `--kueue`          | `-k`      | TEXT    | Local kueue to launch jobs in.                                                                 | `skaha-local-queue`                                                                         |
| `--priority`       | `-p`      | TEXT    | Kueue priority to launch jobs with.                                                            | `high`                                                                                      |
| `--exponent-lower` | `-el`     | INTEGER | Lower bound exponent for job count range `[2^el, ..., 2^eh]`.                                  | `1`                                                                                         |
| `--exponent-higher`| `-eh`     | INTEGER | Higher bound exponent for job count range `[2^el, ..., 2^eh]`.                                  | `3`                                                                                         |
| `--duration`       | `-d`      | INTEGER | Duration for each job in seconds.                                                              | `1`                                                                                         |
| `--cores`          | `-c`      | INTEGER | Number of CPU cores to allocate to each job.                                                   | `1`                                                                                         |
| `--ram`            | `-r`      | INTEGER | Amount of RAM to allocate to each job in GB.                                                   | `1`                                                                                         |
| `--storage`        | `-s`      | INTEGER | Amount of ephemeral-storage to allocate to each job in GB.                                     | `1`                                                                                         |
| `--output`         | `-o`      | TEXT    | File to save results to.                                                                       | `results.csv`                                                                               |
| `--wait`           | `-w`      | INTEGER | Time to wait between experiments.                                                              | `60`                                                                                        |
| `--help`           |           |         | Show this message and exit.                                                                    |                                                                                             |

#### Example Usage



#### Eviction Benchmarks

The eviction benchmark launches a series of jobs with different priority levels and monitors the eviction behavior of Kueue by tailing the events emitted from the Kubernetes API server and analyzes the events to determine if the eviction behavior is as expected. 

**_NOTE_: This benchmark requires a packed cluster queue to test the eviction behavior. For examples, you can modify the `--jobs` parameter in conjunction with the `--cores`, `--ram`, and `--storage` parameters to create a packed cluster queue.** The eviction benchmark will then launch jobs with different priority levels and monitor the eviction behavior of Kueue.

```bash
kr benchmark evictions [OPTIONS]
```

**Options**:
- `-f, --filepath TEXT`: Path to the Kubernetes job template file. Default: `src/kueuer/benchmarks/job.yaml`.
- `-n, --namespace TEXT`: Namespace to launch jobs in. Default: `skaha-workload`.
- `-k, --kueue TEXT`: Name of the Kueue queue to use. Default: `skaha-local-queue`.
- `-p, --priorities TEXT`: Ordered list of Kueue priorities to test. Default: `low, medium, high`.
- `-j, --jobs INTEGER`: Number of jobs per priority level. Default: `8`.
- `-c, --cores INTEGER`: Total number of CPU cores in the cluster queue. Default: `8`.
- `-r, --ram INTEGER`: Total amount of RAM in the cluster queue in GB. Default: `8`.
- `-s, --storage INTEGER`: Total amount of storage in the cluster queue in GB. Default: `8`.
- `-d, --duration INTEGER`: Longest duration for jobs in seconds. Default: `120`.

### Benchmark Results

The results of the benchmarks are saved in CSV format and can be visualized using the `kr plot` command. The performance benchmarks generate metrics such as throughput, latency, and efficiency, while the eviction benchmarks provide insights into priority rule adherence and resource utilization.






## Jobs

Kueuer also provides a simple interface to launch and delete massive number of jobs on a Kubernetes cluster to simulate stress. This is useful for testing the performance of Kueue and Kubernetes job scheduling under heavy load.

### Managing Jobs
To run jobs, use the `kr jobs` command. This command provides two subcommands:

#### `kr jobs run`

### `kr jobs delete`

Run jobs to stress k8s cluster.

**Usage**:

```console
$ kr jobs run [OPTIONS]
```

**Options**:

* `-f, --filepath TEXT`: K8s job template.  [default: /Users/brars/Workspace/opencadc/deployments/configs/kueue/kueuer/src/kueuer/benchmarks/job.yaml]
* `-n, --namespace TEXT`: Namespace to launch jobs in.  [default: default]
* `-p, --prefix TEXT`: Prefix for job names.  [default: kueuer-job]
* `-j, --jobs INTEGER`: Number of jobs to launch.  [default: 1]
* `-d, --duration INTEGER`: Duration for each job in seconds.  [default: 60]
* `-c, --cores INTEGER`: Number of CPU cores to allocate to each job.  [default: 1]
* `-r, --ram INTEGER`: Amount of RAM to allocate to each job in GB.  [default: 1]
* `-s, --storage INTEGER`: Amount of ephemeral-storage to allocate to each job in GB.  [default: 1]
* `-k, --kueue TEXT`: Kueue queue to launch jobs in.
* `-p, --priority TEXT`: Kueue priority to launch jobs with.
* `--help`: Show this message and exit.

#### `kr jobs delete`

Delete jobs with given prefix in a namespace.

Args:
    namespace (str): Namespace to delete jobs in.
    prefix (str): Prefix for job names.

Returns:
    int: Number of jobs deleted

**Usage**:

```console
$ kr jobs delete [OPTIONS]
```

**Options**:

* `-n, --namespace TEXT`: Namespace to launch jobs in.  [default: default]
* `-p, --prefix TEXT`: Prefix for job names.  [default: kueuer-job]
* `--help`: Show this message and exit.

### `kr plot`

Plot Benchmark Results

**Usage**:

```console
$ kr plot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `performance`: Generate visualization plots from...

#### `kr plot performance`

Generate visualization plots from benchmark results.

**Usage**:

```console
$ kr plot performance [OPTIONS]
```

**Options**:

* `-f, --filepath TEXT`: Results CSV File.  [default: results.csv]
* `-o, --output-dir TEXT`: Output directory for plots  [default: ./plots]
* `--log-scale / --no-log-scale`: Use logarithmic scale for x-axis in plots  [default: log-scale]
* `--help`: Show this message and exit.


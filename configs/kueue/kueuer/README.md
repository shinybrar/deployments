# Kueuer

## Command Line Interface
**Usage**:

```console
$ kr [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `benchmark`: Launch Benchmarks
* `jobs`: Launch K8s Jobs
* `plot`: Plot Benchmark Results

### `benchmark`

Launch Benchmarks

**Usage**:

```console
$ kr benchmark [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `performance`: Compare native K8s job scheduling vs.
* `evictions`: Run a benchmark to test eviction behavior...

#### `benchmark performance`

Compare native K8s job scheduling vs. Kueue.

**Usage**:

```console
$ kr benchmark performance [OPTIONS]
```

**Options**:

* `-f, --filepath TEXT`: K8s job template.  [default: /Users/brars/Workspace/opencadc/deployments/configs/kueue/kueuer/src/kueuer/benchmarks/job.yaml]
* `-n, --namespace TEXT`: Namespace to launch jobs in.  [default: skaha-workload]
* `-k, --kueue TEXT`: Local kueue to launch jobs in.  [default: skaha-local-queue]
* `-p, --priority TEXT`: Kueue priority to launch jobs with.  [default: high]
* `-el, --exponent-lower INTEGER`: Lower bound exponent for job count range [2^el, ..., 2^eh].  [default: 1]
* `-eh, --exponent-higher INTEGER`: Higher bound exponent for job count range [2^el, ..., 2^eh].  [default: 3]
* `-d, --duration INTEGER`: Duration for each job in seconds.  [default: 1]
* `-c, --cores INTEGER`: Number of CPU cores to allocate to each job.  [default: 1]
* `-r, --ram INTEGER`: Amount of RAM to allocate to each job in GB.  [default: 1]
* `-s, --storage INTEGER`: Amount of ephemeral-storage to allocate to each job in GB.  [default: 1]
* `-o, --output TEXT`: File to save results to.  [default: results.csv]
* `-w, --wait INTEGER`: Time to wait between experiments.  [default: 60]
* `--help`: Show this message and exit.

#### `benchmark evictions`

Run a benchmark to test eviction behavior of Kueue in a packed cluster queue.

**Usage**:

```console
$ kr benchmark evictions [OPTIONS]
```

**Options**:

* `-f, --filepath TEXT`: K8s job template.  [default: /Users/brars/Workspace/opencadc/deployments/configs/kueue/kueuer/src/kueuer/benchmarks/job.yaml]
* `-n, --namespace TEXT`: Namespace to launch jobs in.  [default: skaha-workload]
* `-k, --kueue TEXT`: Local Kueue queue to launch jobs in.  [default: skaha-local-queue]
* `-p, --priorities TEXT`: Ordered Kueue priorities to launch jobs with, from low to high.  [default: low, medium, high]
* `-j, --jobs INTEGER`: Jobs per priority level to launch.  [default: 8]
* `-c, --cores INTEGER`: Total number of CPU cores in the kueue ClusterQueue.  [default: 8]
* `-r, --ram INTEGER`: Total amount of RAM in the kueue ClusterQueue in GB.  [default: 8]
* `-s, --storage INTEGER`: Total amount of storage in the kueue ClusterQueue in GB.  [default: 8]
* `-d, --duration INTEGER`: Longest duration for jobs in seconds.  [default: 120]
* `--help`: Show this message and exit.

### `jobs`

Launch K8s Jobs

**Usage**:

```console
$ kr jobs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run`: Run jobs to stress k8s cluster.
* `delete`: Delete jobs with given prefix in a namespace.

#### `jobs run`

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

#### `jobs delete`

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

### `plot`

Plot Benchmark Results

**Usage**:

```console
$ kr plot [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `performance`: Generate visualization plots from...

#### `plot performance`

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


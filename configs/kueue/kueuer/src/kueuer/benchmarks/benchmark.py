"""Benchmark module for comparing Kubernetes job execution with and without Kueue."""

import csv
import os
import math
import time
from datetime import datetime
from time import sleep
from typing import Any, Dict, List, Optional, Set

import typer

from kueuer.benchmarks import launch, track
from kueuer.utils.logging import logger

benchmark_cli: typer.Typer = typer.Typer(help="Launch Benchmark Suite")


def experiment(
    count: int,
    duration: int,
    cores: int,
    ram: int,
    storage: int,
    namespace: str,
    filepath: str,
    use_kueue: bool = False,
    kueue: Optional[str] = None,
    priority: Optional[str] = None,
) -> Dict[str, Any]:
    """Run a single experiment with the specified configuration.

    Args:
        job_count: Number of jobs to create
        job_duration: Duration of each job in seconds
        cores: Number of CPU cores per job
        ram: RAM in GB per job
        storage: Storage in GB per job
        namespace: Kubernetes namespace
        template_file: Path to the job template file
        use_kueue: Whether to use Kueue for job queueing
        kueue_queue: Kueue queue name (required if use_kueue is True)
        kueue_priority: Kueue priority (optional, used if use_kueue is True)

    Returns:
        Dict containing experiment results and timing information
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    prefix = f"{'kueue' if use_kueue else 'direct'}-{timestamp}-{count}"
    logger.info("=" * 80)
    logger.info("Starting experiment with %d jobs, duration %ds", count, duration)
    logger.info("Configuration: %s", "With Kueue" if use_kueue else "Direct Kubernetes")
    if use_kueue:
        logger.info("Kueue Queue: %s, Priority: %s", kueue, priority)
    logger.info(
        "Namespace: %s, Cores: %s, RAM: %sGB, Storage: %sGB",
        namespace,
        cores,
        ram,
        storage,
    )
    logger.info("=" * 80)

    # Start measuring time
    start_time = time.time()

    # Execute the launcher
    launch.jobs(
        filepath=filepath,
        namespace=namespace,
        prefix=prefix,
        count=count,
        duration=duration,
        cores=cores,
        ram=ram,
        storage=storage,
        kueue=kueue,
        priority=priority,
    )

    # Track jobs to completion and get timing statistics
    logger.info("Jobs launched, tracking completion...")
    times = track.jobs(namespace, prefix, "Complete")
    logger.info("All jobs completed, computing statistics...")
    stats = track.compute_statistics(times)

    # End time measurement
    end_time = time.time()
    total_execution_time = end_time - start_time

    # Prepare result
    result: Dict[str, Optional[Any]] = {
        "timestamp": timestamp,
        "job_count": count,
        "use_kueue": use_kueue,
        "kueue_queue": kueue if use_kueue else None,
        "kueue_priority": priority if use_kueue else None,
        "job_duration": duration,
        "cores": cores,
        "ram": ram,
        "storage": storage,
        "namespace": namespace,
        "total_execution_time": total_execution_time,
        # Extract values from stats dictionary with fallbacks to None
        "first_creation_time": stats.get("first_creation_time"),
        "last_creation_time": stats.get("last_creation_time"),
        "first_completion_time": stats.get("first_completion_time"),
        "last_completion_time": stats.get("last_completion_time"),
        "avg_time_from_creation_completion": stats.get(
            "avg_time_from_creation_completion"
        ),
        "total_time_from_first_creation_to_last_completion": stats.get(
            "total_time_from_first_creation_to_last_completion"
        ),
        "median_time_from_creation_completion": stats.get(
            "median_time_from_creation_completion"
        ),
        "std_dev_time_from_creation_completion": stats.get(
            "std_dev_time_from_creation_completion"
        ),
    }

    logger.info("Experiment completed in %.2fs", total_execution_time)
    total = result["total_time_from_first_creation_to_last_completion"]
    logger.info("Total time from first creation to last completion: %.2fs", total)

    # Cleanup jobs
    logger.info("Cleaning up jobs...")
    launch.delete_jobs_with_prefix(namespace, prefix)
    return result


def benchmark(
    counts: List[int],
    duration: int,
    cores: int,
    ram: int,
    storage: int,
    namespace: str,
    filepath: str,
    kueue: Optional[str],
    priority: Optional[str],
    resultsfile: str,
    wait: int,
) -> List[Dict[str, Any]]:
    """
    Run a complete benchmark comparing direct Kubernetes jobs vs Kueue jobs.

    Args:
        job_counts: List of job counts to test
        job_duration: Duration of each job in seconds
        cores: Number of CPU cores per job
        ram: RAM in GB per job
        storage: Storage in GB per job
        namespace: Kubernetes namespace
        template_file: Path to the job template file
        kueue_queue: Kueue queue name
        kueue_priority: Kueue priority
        results_file: Path to save results CSV
        wait_between_runs: Time to wait between experiment runs in seconds

    Returns:
        List of dictionaries containing all experiment results
    """
    results: List[Dict[str, Optional[Any]]] = []

    # Ensure job counts are sorted
    counts = sorted(counts)

    for count in counts:
        # Run without Kueue
        result = experiment(
            count=count,
            duration=duration,
            cores=cores,
            ram=ram,
            storage=storage,
            namespace=namespace,
            filepath=filepath,
            use_kueue=False,
        )
        results.append(result)

        # Save intermediate results
        save_results_to_csv(results, resultsfile)

        # Wait between experiments
        logger.info("Waiting %ss before next experiment...", wait)
        sleep(wait)

        # Run with Kueue
        kueue_result = experiment(
            count=count,
            duration=duration,
            cores=cores,
            ram=ram,
            storage=storage,
            namespace=namespace,
            filepath=filepath,
            use_kueue=True,
            kueue=kueue,
            priority=priority,
        )
        results.append(kueue_result)

        # Save intermediate results
        save_results_to_csv(results, resultsfile)

        # Wait between experiments
        if count != counts[-1]:  # Don't wait after the last experiment
            logger.info("Waiting %s seconds before next experiment...", wait)
            sleep(wait)

    return results


def save_results_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """
    Save benchmark results to a CSV file.

    Args:
        results: List of experiment result dictionaries
        filename: Path to save CSV file
    """
    # Define fieldnames based on all possible keys in results
    fieldnames: Set[str] = set()
    for result in results:
        fieldnames.update(result.keys())
    fieldnames = sorted(fieldnames)  # type: ignore

    # Check if file exists to determine if header is needed
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for result in results:
            # Handle datetime objects by converting them to strings
            row_data = {}
            for key, value in result.items():
                if isinstance(value, datetime):
                    row_data[key] = value.isoformat()
                else:
                    row_data[key] = value
            writer.writerow(row_data)

    logger.info("Results saved to %s", filename)


@benchmark_cli.command("performance")
def performance(
    filepath: str = (typer.Option(..., "-f", "--filepath", help="K8s job template.")),
    namespace: str = (
        typer.Option(..., "-n", "--namespace", help="Namespace to launch jobs in.")
    ),
    kueue: str = (
        typer.Option(..., "-k", "--kueue", help="Local kueue to launch jobs in.")
    ),
    priority: str = (
        typer.Option(
            ..., "-p", "--priority", help="Kueue priority to launch jobs with."
        )
    ),
    e0: int = typer.Option(
        4,
        "-e0",
        "--exponent0",
        help="Lower bound exponent for to create jobs [2^e0, ..., 2^e])",
    ),
    exponent: int = typer.Option(
        10,
        "-e",
        "--exponent",
        help="Upper bound for to create jobs [2^e0, ..., 2^e])",
    ),
    duration: int = (
        typer.Option(1, "-d", "--duration", help="Duration for each job in seconds.")
    ),
    cores: int = (
        typer.Option(
            1, "-c", "--cores", help="Number of CPU cores to allocate to each job."
        )
    ),
    ram: int = (
        typer.Option(
            1, "-r", "--ram", help="Amount of RAM to allocate to each job in GB."
        )
    ),
    storage: int = (
        typer.Option(
            1,
            "-s",
            "--storage",
            help="Amount of ephemeral-storage to allocate to each job in GB.",
        )
    ),
    output: str = (
        typer.Option("results.csv", "-o", "--output", help="File to save results to.")
    ),
    wait: int = (
        typer.Option(60, "-w", "--wait", help="Time to wait between experiments.")
    ),
):
    """Run a benchmark comparing native K8s job scheduling performance against Kueue."""
    counts = [2**i for i in range(e0, exponent + 1)]
    logger.info("Starting benchmark with the following configuration:")
    logger.info("Jobs     : %s", counts)
    logger.info("Duration : %ss", duration)
    logger.info("Cores    : %s, RAM: %sGB, Storage: %sGB", cores, ram, storage)
    logger.info("Namespace: %s", namespace)
    logger.info("Template : %s", filepath)
    logger.info("Kueue    : %s", kueue)
    logger.info("Priority : %s", priority)
    logger.info("Output   : %s", output)
    logger.info("Wait     : %ss", wait)

    benchmark(
        counts=counts,
        duration=duration,
        cores=cores,
        ram=ram,
        storage=storage,
        namespace=namespace,
        filepath=filepath,
        kueue=kueue,
        priority=priority,
        resultsfile=output,
        wait=wait,
    )
    logger.info("Benchmark completed successfully.")
    logger.info("Results saved to %s", output)
    logger.info("You can now run 'kueuer plot performance' to visualize the results.")


@benchmark_cli.command("evictions")
def eviction(
    filepath: str = (typer.Option(..., "-f", "--filepath", help="K8s job template.")),
    namespace: str = (
        typer.Option(..., "-n", "--namespace", help="Namespace to launch jobs in.")
    ),
    kueue: str = (
        typer.Option(..., "-k", "--kueue", help="Local Kueue queue to launch jobs in.")
    ),
    priorities: List[str] = (
        typer.Option(
            ["low", "medium", "high"],
            "-p",
            "--priorities",
            help="Ordered Kueue priorities to launch jobs with, from low to high.",
        )
    ),
    jobs: int = (
        typer.Option(8, "-j", "--jobs", help="Jobs per priority level to launch.")
    ),
    cores: int = (
        typer.Option(
            8,
            "-c",
            "--cores",
            help="Total number of CPU cores in the kueue ClusterQueue.",
        )
    ),
    ram: int = (
        typer.Option(
            8,
            "-r",
            "--ram",
            help="Total amount of RAM in the kueue ClusterQueue in GB.",
        )
    ),
    storage: int = (
        typer.Option(
            8,
            "-s",
            "--storage",
            help="Total amount of storage in the kueue ClusterQueue in GB.",
        )
    ),
    duration: int = (
        typer.Option(120, "-d", "--duration", help="Longest duration for jobs in seconds.")
    )
):
    """Run a benchmark to test eviction behavior of Kueue in a packed cluster queue." """
    logger.info("Starting eviction benchmarks with the following configuration:")
    logger.info("Template     : %s", filepath)
    logger.info("Namespace    : %s", namespace)
    logger.info("Kueue        : %s", kueue)
    logger.info("Priorities   : %s", priorities)
    logger.info("Total Cores  : %s", cores)
    logger.info("Total RAM    : %sGB", ram)
    logger.info("Total Storage: %sGB", storage)

    prefix: str = "kueue-eviction"
    job_count = jobs
    job_core: int = math.ceil(cores / job_count)
    job_ram: int = math.ceil(ram / job_count)
    job_storage: int = math.ceil(storage / job_count)

    for index, priority in enumerate(priorities):
        job_duration = max(int(duration / (2 ** index)), 1)
        logger.info("Job Parameters: Cores: %s, RAM: %sGB, Storage: %sGB", job_core, job_ram, job_storage)
        logger.info("Launching %s jobs with %s priority and duration of %ss" , job_count, priority, job_duration)
        launch.jobs(
            filepath=filepath,
            namespace=namespace,
            prefix=f"{prefix}-{priority}-job",
            count=job_count,
            duration=job_duration,
            cores=job_core,
            ram=job_ram,
            storage=job_storage,
            kueue=kueue,
            priority=priority,
        )

    logger.info("All jobs launched successfully.")
    logger.info("Tracking jobs to completion...")
    data: Dict[str, Any] = {}
    for priority in reversed(priorities):
        prefix = f"{prefix}-{priority}-job"
        data[priority] = track.jobs(namespace, prefix, "Complete")
    logger.info("All jobs completed, computing statistics...")
    stats: Dict[str, Any] = {}
    
    for priority in priorities:
        stats[priority] = track.compute_statistics(data[priority])
    
    logger.info("Saving statistics to CSV...")
    for priority in priorities:
        save_results_to_csv(stats[priority], f"{prefix}-{priority}-stats.csv")
    



    # Eviction Benchmark
    # 1. Create long running jobs packing the cluster queue
    # 2. Create a new shortlived higher priority job using minimum resources
    # 3. Confirm if a workload is evicted
    # 4. Confirm if the higher priority job is executed
    # 5. Cleanup
    pass


if __name__ == "__main__":
    benchmark_cli()

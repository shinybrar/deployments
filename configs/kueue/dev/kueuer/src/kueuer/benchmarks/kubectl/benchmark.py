"""Benchmark module for comparing Kubernetes job execution with and without Kueue."""

import csv
import os
import time
from datetime import datetime
from time import sleep
from typing import Annotated, Any, Dict, List, Optional

import typer

from kueuer.jobs import launcher, tracker

app = typer.Typer(help="Kueuer Job Benchmark")


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
    """
    Run a single experiment with the specified configuration.

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

    print(f"\n{'='*80}")
    print(f"Starting experiment with {count} jobs, duration {duration}s")
    print(f"Configuration: {'With Kueue' if use_kueue else 'Direct Kubernetes'}")
    if use_kueue:
        print(f"Kueue Queue: {kueue}, Priority: {priority}")
    print(f"Namespace: {namespace}, Cores: {cores}, RAM: {ram}GB, Storage: {storage}GB")
    print(f"{'='*80}")

    # Start measuring time
    start_time = time.time()

    # Execute the launcher
    launcher.main(
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
    print("Jobs launched, tracking completion...")
    times = tracker.for_completion(namespace, prefix)
    stats = tracker.compute_statistics(times)

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

    print(f"Experiment completed in {total_execution_time:.2f}s")
    print(
        f"Total time from first creation to last completion: {result['total_time_from_first_creation_to_last_completion']:.2f}s"
    )

    # Cleanup jobs
    print("Cleaning up jobs...")
    launcher.delete_jobs_with_prefix(namespace, prefix, dry_run=False)

    return result


def benchmark(
    counts: List[int],
    duration: int,
    cores: int,
    ram: int,
    storage: int,
    namespace: str,
    filepath: str,
    kueue: str,
    priority: str,
    resultsfile: str,
    wait: int,
    cleanup: bool,
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
        print(f"Waiting {wait} seconds before next experiment...")
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
            print(f"Waiting {wait} seconds before next experiment...")
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
    fieldnames = set()
    for result in results:
        fieldnames.update(result.keys())
    fieldnames = sorted(fieldnames)

    # Check if file exists to determine if header is needed
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as csvfile:
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

    print(f"Results saved to {filename}")


@app.command()
def main(
    filepath: str = (typer.Option(..., "-f", "--filepath", help="K8s job template.")),
    namespace: str = (
        typer.Option(..., "-n", "--namespace", help="Namespace to launch jobs in.")
    ),
    counts: Annotated[
        List[int], typer.Option("-c", "--counts", help="Number of jobs to launch.")
    ] = [2, 4, 8],
    duration: int = (
        typer.Option(1, "-d", "--duration", help="Duration for each job in seconds.")
    ),
    cores: int = (
        typer.Option(1, "--cores", help="Number of CPU cores to allocate to each job.")
    ),
    ram: int = (
        typer.Option(1, "--ram", help="Amount of RAM to allocate to each job in GB.")
    ),
    storage: int = (
        typer.Option(
            1,
            "--storage",
            help="Amount of ephemeral-storage to allocate to each job in GB.",
        )
    ),
    kueue: str = (typer.Option(..., "--kueue", help="Kueue queue to launch jobs in.")),
    priority: str = (
        typer.Option(
            ..., "--kueue-priority", help="Kueue priority to launch jobs with."
        )
    ),
    resultfile: str = (
        typer.Option("results.csv", "--results-file", help="File to save results to.")
    ),
    wait: int = (
        typer.Option(
            60, "--wait-between-runs", help="Time to wait between experiments."
        )
    ),
    cleanup: bool = (
        typer.Option(
            True, "--cleanup", help="Delete all jobs and pods after each experiment."
        )
    ),
):
    print("Starting benchmark with the following configuration:")
    print(f"Job counts: {counts}")
    print(f"Job duration: {duration}s")
    print(f"Cores: {cores}, RAM: {ram}GB, Storage: {storage}GB")
    print(f"Namespace: {namespace}")
    print(f"Template file: {filepath}")
    print(f"Kueue queue: {kueue}")
    print(f"Kueue priority: {priority}")
    print(f"Results file: {resultfile}")
    print(f"Wait between runs: {wait}s")

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
        resultsfile=resultfile,
        wait=wait,
        cleanup=cleanup,
    )
    print("Benchmark completed successfully.")
    print(f"Results saved to {resultfile}")
    print("You can now run 'python -m kueuer.plot' to visualize the results.")


if __name__ == "__main__":
    app()

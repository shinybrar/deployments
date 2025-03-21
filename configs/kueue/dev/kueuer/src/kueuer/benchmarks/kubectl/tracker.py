import statistics
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from kubernetes import client, config

# Type alias for job tracking: (creation_time, completion_time, duration_in_seconds)
JobTiming = Tuple[datetime, Optional[datetime], Optional[float]]


def job_is_done(job: client.V1Job, desired_status: str) -> bool:
    """
    Checks if the job has a condition matching the desired_status (e.g. 'Complete')
    with a True status.
    """
    if job.status.conditions:
        for condition in job.status.conditions:
            if condition.type == desired_status and condition.status == "True":
                print(f"Job '{job.metadata.name}' reached '{desired_status}'")
                return True
    return False


def compute_statistics(done_jobs: Dict[str, JobTiming]) -> Dict[str, Any]:
    """Compute Job Statistics"""
    creation_times: List[datetime] = [
        data[0] for data in done_jobs.values() if data[0] is not None
    ]
    completion_times: List[datetime] = [
        data[1] for data in done_jobs.values() if data[1] is not None
    ]
    durations: List[float] = [
        data[2] for data in done_jobs.values() if data[2] is not None
    ]

    if not creation_times or not completion_times or not durations:
        return {}

    first_creation_time: datetime = min(creation_times)
    last_creation_time: datetime = max(creation_times)
    first_completion_time: datetime = min(completion_times)
    last_completion_time: datetime = max(completion_times)
    avg_duration: float = statistics.mean(durations)
    total_duration: float = (last_completion_time - first_creation_time).total_seconds()
    median_duration: float = statistics.median(durations)
    stddev_duration: float = statistics.stdev(durations) if len(durations) > 1 else 0.0

    stats: Dict[str, Any] = {
        "first_creation_time": first_creation_time,
        "last_creation_time": last_creation_time,
        "first_completion_time": first_completion_time,
        "last_completion_time": last_completion_time,
        "avg_time_from_creation_completion": avg_duration,
        "total_time_from_first_creation_to_last_completion": total_duration,
        "median_time_from_creation_completion": median_duration,
        "std_dev_time_from_creation_completion": stddev_duration,
    }
    return stats


def for_completion(
    namespace: str,
    prefix: str,
    desired_status: str = "Complete",
    poll_interval: int = 30,
) -> Dict[str, JobTiming]:
    """
    Tracks jobs in the specified namespace whose names start with the given prefix.
    Polls only the pending jobs until all have reached the desired terminal condition.
    Returns a dictionary of completed jobs with each value as a tuple:
    (creation_time, completion_time, duration_in_seconds).
    """
    config.load_kube_config()

    batch_v1: client.BatchV1Api = client.BatchV1Api()

    # Step 1: Fetch all jobs once.
    print(f"Fetching jobs with prefix '{prefix}' in namespace '{namespace}'")
    pending: Dict[str, datetime] = {}
    done: Dict[str, JobTiming] = {}

    for job in batch_v1.list_namespaced_job(namespace=namespace).items:
        if job.metadata.name.startswith(prefix):
            creation_time: datetime = job.metadata.creation_timestamp
            pending[job.metadata.name] = creation_time

    if not pending:
        print("No jobs found with the given prefix.")
        return done

    while len(pending) > 0:
        print(f"Tracking {len(pending)} jobs...")
        # Iterate over a copy of keys to avoid mutation issues.
        for job in batch_v1.list_namespaced_job(namespace=namespace).items:
            job_name: str = job.metadata.name
            if job_name not in pending:
                continue

            if job_is_done(job, desired_status):
                completion_time: datetime = job.status.completion_time
                creation_time: datetime = pending[job_name]
                duration: float = (completion_time - creation_time).total_seconds()
                print(
                    f"Job '{job_name}' reached '{desired_status}' in {duration:.2f} seconds."
                )
                done[job_name] = (creation_time, completion_time, duration)
                # Step 3: Move job from pending to done.
                del pending[job_name]

        # Step 4: Re-check only pending jobs.
        if len(pending) > 0:
            print(f"Waiting for {len(pending)} jobs to reach '{desired_status}'...")
            print("Sleeping for a while, Zzz...{poll_interval}s")
            time.sleep(poll_interval)

    return done

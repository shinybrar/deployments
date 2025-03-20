"""Launches a job in a Kubernetes cluster."""

import asyncio
from copy import deepcopy
from typing import Any, Awaitable, Dict, List, Optional

import aiofiles
import typer
import yaml
import subprocess

app = typer.Typer(help="Kueuer Job Launcher")


def template(filepath: str) -> Dict[Any, Any]:
    """K8s job template.

    Args:
        filepath (str): Path to the K8s job template.

    Returns:
        Dict[Any, Any]: K8s job template.
    """
    with open(filepath, encoding="utf-8") as f:
        data = f.read()
        return yaml.safe_load(data)


async def run(data: Dict[Any, Any], name: str) -> str:
    """Runs a job in a Kubernetes cluster.

    Args:
        data (Dict[Any, Any]): K8s job template.
        name (str): Name of the job.

    Returns:
        str: _description_
    """
    data["metadata"]["name"] = name
    for container in data["spec"]["template"]["spec"]["containers"]:
        container["name"] = name
    async with aiofiles.tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".yaml"
    ) as temp:
        await temp.write(yaml.dump(data))

    command = f"kubectl apply -f {temp.name}"
    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()
    return str(temp.name)


def delete_jobs_with_prefix(namespace: str, prefix: str, dry_run: bool = False):
    """
    Delete all Kubernetes jobs in a specific namespace with a given prefix.

    Args:
        namespace (str): Kubernetes namespace containing the jobs
        prefix (str): Prefix to filter jobs by
        dry_run (bool): If True, only print jobs that would be deleted without actually deleting

    Returns:
        int: Number of deleted jobs
    """
    # Get all jobs in the namespace
    cmd = [
        "kubectl",
        "get",
        "jobs",
        "-n",
        namespace,
        "--no-headers",
        "-o",
        "custom-columns=:metadata.name",
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        jobs = result.stdout.strip().split("\n")

        # Filter jobs by prefix
        jobs_to_delete = [job for job in jobs if job and job.startswith(prefix)]

        if not jobs_to_delete:
            print(f"No jobs with prefix '{prefix}' found in namespace '{namespace}'")
            return 0

        print(
            f"Found {len(jobs_to_delete)} jobs with prefix '{prefix}' in namespace '{namespace}'"
        )

        if dry_run:
            return 1

        # Delete each job
        for job in jobs_to_delete:
            delete_cmd = ["kubectl", "delete", "job", "-n", namespace, job]
            subprocess.run(delete_cmd, check=True, capture_output=True, text=True)
            print(f"Deleted job: {job}")

        return len(jobs_to_delete)

    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command: {e}")
        print(f"Error output: {e.stderr}")
        return 0


@app.command()
def main(
    filepath: str = (typer.Option(..., "-f", "--filepath", help="K8s job template.")),
    namespace: str = (
        typer.Option(..., "-n", "--namespace", help="Namespace to launch jobs in.")
    ),
    prefix: str = typer.Option(
        "kueuer-job", "-p", "--prefix", help="Prefix for job names."
    ),
    count: int = (typer.Option(1, "-c", "--count", help="Number of jobs to launch.")),
    duration: int = (
        typer.Option(60, "-d", "--duration", help="Duration for each job in seconds.")
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
    kueue: Optional[str] = (
        typer.Option(None, "--kueue", help="Kueue queue to launch jobs in.")
    ),
    priority: Optional[str] = (
        typer.Option(
            None, "--kueue-priority", help="Kueue priority to launch jobs with."
        )
    ),
):
    """Stress Test Kubernetes Cluster."""
    ram_mb: float = ram * 1024.0
    args: List[str] = [
        "--cpu",
        f"{cores}",
        "--cpu-method",
        "matrixprod",
        "--vm",
        "1",
        "--vm-bytes",
        f"{ram_mb*0.8}M",
        "--temp-path",
        "/tmp",
        "--timeout",
        f"{duration}",
        "--metrics-brief",
    ]
    job = template(filepath)

    # Write common job parameters
    job["metadata"] = {}
    job["metadata"]["labels"] = {}
    job["metadata"]["namespace"] = namespace
    if kueue:
        job["metadata"]["labels"]["kueue.x-k8s.io/queue-name"] = kueue
    if priority:
        job["metadata"]["labels"]["kueue.x-k8s.io/priority-class"] = priority
    for container in job["spec"]["template"]["spec"]["containers"]:
        container["args"] = args
        container["resources"] = {}
        container["resources"]["limits"] = {}
        container["resources"]["limits"]["cpu"] = f"{cores}"
        container["resources"]["limits"]["memory"] = f"{ram_mb}Mi"
        container["resources"]["limits"]["ephemeral-storage"] = f"{storage}Gi"
        container["resources"]["requests"] = {}
        container["resources"]["requests"]["cpu"] = f"{cores}"
        container["resources"]["requests"]["memory"] = f"{ram_mb}Mi"
        container["resources"]["requests"]["ephemeral-storage"] = f"{storage}Gi"

    tasks: List[Awaitable[str]] = []

    for num in range(count):
        name: str = f"{prefix}-{num}"
        config = deepcopy(job)
        tasks.append(run(config, name))

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    app()

"""Launches a job in a Kubernetes cluster."""

import asyncio
from time import time
from typing import Any, Awaitable, Dict, List, Optional

import aiofiles
import aiofiles.os
import typer
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = typer.Typer(help="Launch Jobs")


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


async def run(data: Dict[Any, Any], prefix: str, count: int) -> bool:
    """Runs a job in a Kubernetes cluster.

    Args:
        data (Dict[Any, Any]): K8s job template.
        name (str): Name of the job.

    """
    async with aiofiles.tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".yaml"
    ) as temp:
        for num in range(count):
            name: str = f"{prefix}-{num}"
            data["metadata"]["name"] = name
            for container in data["spec"]["template"]["spec"]["containers"]:
                container["name"] = name
            await temp.write(yaml.dump(data))
            await temp.write("\n---\n")
    print(f"Applying {temp.name}")
    now = time()
    try:
        command = f"kubectl apply -f {temp.name}"
        proc = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        print(f"stdout: {stdout.decode()}")
        print(f"stderr: {stderr.decode()}")
        return True
    finally:
        print(f"Took {time()- now} seconds to apply {temp.name}")
        print(f"Deleting {temp.name}")
        await temp.close()
        await aiofiles.os.remove(str(temp.name))


def delete_jobs_with_prefix(namespace: str, prefix: str) -> int:
    """Deletes all jobs with a given prefix in a namespace.

    Args:
        namespace (str): Namespace to delete jobs in.
        prefix (str): Prefix for job names.

    Returns:
        int: Number of jobs deleted
    """
    config.load_kube_config()

    batch_v1 = client.BatchV1Api()

    try:
        jobs = batch_v1.list_namespaced_job(namespace)
        jobs_to_delete = [
            job.metadata.name
            for job in jobs.items
            if job.metadata.name.startswith(prefix)
        ]

        if not jobs_to_delete:
            print(f"No jobs with prefix '{prefix}' found in namespace '{namespace}'")
            return 0
        num = len(jobs_to_delete)
        print(f"Found {num} jobs with prefix '{prefix}' in namespace '{namespace}'")
        for job_name in jobs_to_delete:
            batch_v1.delete_namespaced_job(
                name=job_name,
                namespace=namespace,
                body=client.V1DeleteOptions(propagation_policy="Foreground"),
            )
        return len(jobs_to_delete)
    except ApiException as e:
        print(f"Exception when deleting jobs: {e}")
        return 0


@app.command("jobs")
def jobs(
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

    tasks: List[Awaitable[bool]] = []
    tasks.append(run(job, prefix, count))
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    app()

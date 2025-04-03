"""Benchmarking job for Kueuer."""

from pathlib import Path

DEFAULT_JOBSPEC_FILEPATH: str = (
    Path(__file__).resolve().parent / "job.yaml"
).as_posix()
DEFAULT_NAMESPACE: str = "skaha-workload"
DEFAULT_KUEUE: str = "skaha-local-queue"
DEFAULT_KUEUE_PRIORITY: str = "high"
DEFAULT_JOB_PREFIX: str = "kueuer-job"

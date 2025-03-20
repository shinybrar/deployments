from typing import Optional

from kubernetes.client import (
    V1Capabilities,
    V1Container,
    V1EmptyDirVolumeSource,
    V1Job,
    V1JobSpec,
    V1NodeAffinity,
    V1NodeSelector,
    V1NodeSelectorRequirement,
    V1NodeSelectorTerm,
    V1ObjectMeta,
    V1PodSecurityContext,
    V1PodSpec,
    V1PodTemplateSpec,
    V1ResourceRequirements,
    V1SeccompProfile,
    V1SecurityContext,
    V1Volume,
)
from pydantic import BaseModel, Field


class Job(BaseModel):
    image: str = Field(..., description="Container image for the job")
    name: str = Field(..., description="Name of the job")
    command: list[str] = Field(..., description="Command to run in the container")
    args: list[str] = Field(..., description="Arguments to pass to the command")
    cores: int = Field(1, description="Number of CPU cores to allocate", gt=1, le=64)
    ram: int = Field(1, description="Amount of RAM to allocate in GB", gt=1, le=128)
    namespace: str = Field(
        "canfar-b-workload", description="Namespace to deploy the job in", frozen=True
    )
    storage: int = Field(
        1, description="Amount of ephemeral storage to allocate in GB", gt=1, le=128
    )
    kueue: Optional[str] = Field(
        None, description="Name of the Kubernetes queue to submit the job to"
    )
    priority: Optional[str] = Field(None, description="Priority of the job")

    def resources(self) -> V1ResourceRequirements:
        return V1ResourceRequirements(
            requests={
                "cpu": f"{self.cores}",
                "memory": f"{self.ram}Gi",
                "ephemeral-storage": f"{self.storage}Gi",
            },
            limits={
                "cpu": f"{self.cores}",
                "memory": f"{self.ram}Gi",
                "ephemeral-storage": f"{self.storage}Gi",
            },
        )

    def labels(self) -> dict[str, str]:
        labels: dict[str, str] = {}
        if self.kueue:
            labels["kueue.x-k8s.io/queue-name"] = self.kueue
        if self.priority:
            labels["kueue.x-k8s.io/priority-class"] = self.priority
        return labels

    def container(self) -> V1Container:
        return V1Container(
            name=self.name,
            image=self.image,
            image_pull_policy="IfNotPresent",
            command=[self.command],
            args=self.args,
            resources=self.resources(),
            security_context=V1SecurityContext(
                allow_privilege_escalation=False,
                privileged=False,
                capabilities=V1Capabilities(drop=["ALL"]),
            ),
        )

    def volumes(self) -> list[V1Volume]:
        volumes: list[V1Volume] = [
            V1Volume(
                name="scratch-dir",
                empty_dir=V1EmptyDirVolumeSource(),
            )
        ]
        return volumes

    def affinity(self) -> V1NodeAffinity:
        return V1NodeAffinity(
            required_during_scheduling_ignored_during_execution=V1NodeSelector(
                node_selector_terms=[
                    V1NodeSelectorTerm(
                        match_expressions=[
                            V1NodeSelectorRequirement(
                                key="skaha.opencadc.org/node-type",
                                operator="NotIn",
                                values=["service-node"],
                            )
                        ]
                    )
                ]
            )
        )

    def metadata(self) -> V1ObjectMeta:
        return V1ObjectMeta(
            name=self.name,
            labels=self.labels(),
        )

    def podspec(self) -> V1PodSpec:
        return V1PodSpec(
            containers=[self.container()],
            restart_policy="Never",
            affinity=self.affinity(),
            security_context=V1PodSecurityContext(
                run_as_user=99999,
                run_as_group=99999,
                fs_group=99999,
                run_as_non_root=True,
                supplemental_groups=[99999],
                seccomp_profile=V1SeccompProfile(type="RuntimeDefault"),
            ),
            automount_service_account_token=False,
            termination_grace_period_seconds=30,
            volumes=self.volumes(),
        )

    def template(self) -> V1PodTemplateSpec:
        return V1PodTemplateSpec(
            metadata=self.metadata(),
            spec=self.podspec(),
        )

    def jobspec(self) -> V1JobSpec:
        return V1JobSpec(
            template=self.template(),
            backoff_limit=0,
            completion_mode="NonIndexed",
            completions=1,
            parallelism=1,
            suspend=False,
            ttl_seconds_after_finished=3600,
            active_deadline_seconds=7200,
        )

    def job(self) -> V1Job:
        metadata = self.metadata()
        metadata.namespace = self.namespace
        return V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=metadata,
            spec=self.jobspec(),
        )

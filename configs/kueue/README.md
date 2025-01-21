# K8s Kueue on Science Platform

_This documentation and design consideration are based on kueue v0.10.0._

## Overview

Kueue is a kubernetes-native system that manages resources, quotas and queues for workloads.

When Kueue is enabled for a kubernetes namespace where a workload is launched, it is launched in a `Suspended` [Pod Phase](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase) rather than the nominal `Pending` state. This allows Kueue to manage the workload based on the resource, quota, priority and queue rulesets created by the cluster administrator. When all conditions are met, Kueue injects the `nodeAffinity` and releases the workload into a `Pending` state for the kubernetes job controller to manage.

In short, kueue intercepts the workload, and releases it when the cluster is ready to accept it, thus alleviating the pressure from the kubernetes control plane and apiservers, while also providing a lot of flexibility in how workloads are managed.

## Installation Guide

We strongly recommend using the helm chart provided by the kubernetes-sigs/kueue project to install the system in your cluster, found [here](https://github.com/kubernetes-sigs/kueue/tree/main/charts/kueue).

The kueue installation requires a helm `values.yaml` file to be provided during installation. A sample values file is provided with this work.

### Deployment Configuration

The kueue deployment configuration is the cluster environment in which the kueue system is deployed. Along with the controller configuration, all these are defined in the `values.yaml` file.

- Enable prometheus metrics for the kueue controller. This provides a lot of insight into the state of the controller and the queues.
  ```yaml
  enablePrometheus: true
  ```
- Teams can individually enable or disable any kueue `controllerManager.featureGates` as needed. For example, even though enabled by default,

### Controller Configuration

The kueue controller configuration is defined under the `managerConfig.controllerManagerConfigYaml` key in the helm values file. The following changes are recommended to the default values provided by the kueue helm chart:

- Explicitly set the kueue controller to not manage jobs that do not have kueue.x-k8s.io/queue-name annotation set. This ensures that jobs that are not managed by kueue are not intercepted by the system.
  ```yaml
  manageJobsWithoutQueueName: false
  ```

- It is highly recommend enabling metrics for cluster queues, as this provides a lot of insight into the state of the cluster and the queues.
  ```yaml
  metrics.enableClusterQueueResources: true
  ```

- It is highly recommended to initially only enable kueue for `batch/job` workloads to be reconciled by kueue and disable it for workloads, e.g. `StatefulSet, Deployment, DaemonSet, etc`.
  ```yaml
  integrations:
    frameworks:
        - "batch/job"
  ```

- We recommend setting the `namespaceSelector` to exclude the `kube-system` and `kueue-system` namespaces, and include only `skaha-workload` namespace. Coupled with `integrations.framework`, this will ensure that only `batch/jobs` in the `skaha-workload` namespace are reconciled by kueue.
  ```yaml
  integrations:
    ...
    podOptions:
      namespaceSelector:
        matchExpressions:
          - key: kubernetes.io/metadata.name
            operator: NotIn
            values: [ kube-system, kueue-system ]
          - key: kubernetes.io/metadata.name
            operator: In
            values: [ skaha-workload ]
  ```

  ### Installation Steps

  After reading through the configuration guide, follow the steps below to install kueue in your cluster:

  ```bash
  git clone https://github.com/kubernetes-sigs/kueue.git
  cd kueue/charts/kueue
  helm install kueue . -f configs/kueue/dev/values.yaml -n kueue-system
  ```

## Configuration Guide

There are four main components to configure in kueue before it can be used for the Science Platform:

1. `ResourceFlavors` are objects to specify hardware configurations of resources (e.g., CPU, memory) available in your cluster.
2. `ClusterQueues` are objects to manage and distribute resources among various workloads.
3. `LocalQueues` are objects to assign workloads to the appropriate `ClusterQueue` within specific namespaces.
4. `WorkloadPriorityClass` defines the prority of the workload without affecting the pod priority.
5. Science Platform Integration for kueue resource objects.

### [1. ResourceFlavors](https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/)

ResourceFlavors are objects that define the hardware configurations of resources available in your cluster. For example, shown below is a `ResourceFlavor` object that defines a GPU resource flavor mapping to a node label `instance-type: gpu`.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "gpu"
spec:
  nodeLabels:
    instance-type: gpu
```

You can can also create a `ResourceFlavor` fine-tuned to any specific hardware configuration. For example, shown below is a `ResourceFlavor` object that defines a `nvidia-gpu` resource flavor mapping to specific nodes which have `nvidia.com/gpu.product` with values `NVIDIA-A100-PCIE-40GB-MIG-3g.20gb` and `GRID-V100D-16C`.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: nvidia-gpu
spec:
  nodeLabels:
    matchExpressions:
      - key: nvidia.com/gpu.product
        operator: In
        values: [ NVIDIA-A100-PCIE-40GB-MIG-3g.20gb, GRID-V100D-16C ]
```

Alternatively, if your hardware is homogenous across the cluster, or if you no preferences for any specific hardware informed queuing, you can create a `ResourceFlavor` object that maps to all nodes in the cluster. For example, shown below is a `ResourceFlavor` object that defines a `default` resource flavor mapping to all nodes in the cluster.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
```

### [2. ClusterQueues](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/)

`ClusterQueues` govern resources (defined by `ResourceFlavors`) and distribute them among various workloads at a cluster level. A ClusterQueue can draw resources from multiple `ResourceFlavor` objects and share (borrow & lend) them amongst other `ClusterQueues` in the same cohort while respecting workload priorities, job ordering, preemption, and fairness.


For example, shown below are two `ClusterQueues` objects that use resources defined by the `ResourceFlavor` objects created in the previous step.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
    name: "standard-queue"
spec:
  namespaceSelector: {} # match all.
  # Queueing strategy to use.
  queueingStrategy: BestEffortFifo
  # Collection of clusterQueues that can borrow/lend resources among themselves.
  cohort: "collective-cohort"
  # Resources governed by the clusterQueue.
  resourceGroups:
  - coveredResources: ["cpu", "memory", "pods"]
    flavors:
    # Draws resources from the default resource flavor.
    - name: "default"
      # Can use upto 10 CPUs.
      resources:
      - name: "cpu"
        nominalQuota: 10
        borowingLimit: 2
        lendingLimit: 2
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort: Never
    withinClusterQueue: LowerPriority
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
    name: "gpu-queue"
spec:
  namespaceSelector: {} # match all.
  queueingStrategy: BestEffortFifo
  cohort: "collective-cohort"
  resourceGroups:
  - coveredResources: ["nvidia.com/gpu"]
    flavors:
    # Draws resources from the nvidia-gpu resource flavor.
    - name: "nvidia-gpu"
      # Can use upto 2 GPUs.
      resources:
      - name: "nvidia.com/gpu"
        nominalQuota: 10
        borowingLimit: 1
        lendingLimit: 1
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort: Never
    withinClusterQueue: LowerPriority
```

In the example, both `ClusterQueues` objects are part of the same `cohort` and can borrow and lend resources among themselves.


### [3. LocalQueues](https://kueue.sigs.k8s.io/docs/concepts/local_queue/)

`LocalQueues` are simply a namespaces representation of the `ClusterQueue` objects. They assign workloads to the appropriate `ClusterQueue` within specific namespaces. For example, shown below is a `LocalQueue` object that assigns workloads in the `skaha-workload` namespace to the `collective-queue` `ClusterQueue` object.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: skaha-workload
  name: skaha-queue
spec:
  clusterQueue: standard-queue
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: skaha-workload
  name: skaha-gpu-queue
spec:
  clusterQueue: gpu-queue
```

### [4. WorkloadPriorityClass](https://kueue.sigs.k8s.io/docs/concepts/workload_priority_class/)

`WorkloadPriorityClass` defines the priority of the workload without affecting the pod priority. For example, shown below is a `WorkloadPriorityClass` object that defines a `high` priority class with a `priority` of `1000`.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: high
value: 10000
description: "high priority"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: low
value: 100
description: "low priority"
```

### 5. Science Platform Integration

In order to integrate kueue with the Science Platform's `Skaha` service, the following environment variables must be set for the `skaha` service pods,


```yaml
KUEUE_ENABLED: bool
```
Where `KUEUE_ENABLED` is a boolean value that blanket enables or disables kueue for the `skaha-workload` namespace.

```yaml
KUEUE_CONFIG: {}
```
`KUEUE_CONFIG` is a dictionary where the key values are name of the possible kinds of workloads that can be submitted to the science platform, i.e.  `notebook`, `carta`, `desktop`, `contributed`, `headless`, and `default`. The `default` key is a special case, which overrides the kueue config, when a specific workload type is not defined in the `KUEUE_CONFIG` object. Each of these keys need an object defining the `localQueue` and `priorityClass` for the workload type.

For example, shown below is a `KUEUE_CONFIG` object that defines the `queueName` and `priorityClass` for the `notebook` and `default` workload types. Since the `carta`, `desktop`, `contributed`, and `headless` workload types are not defined in the `KUEUE_CONFIG` object, the `default` key is used to define the `queueName` and `priorityClass` for these workload types.

```yaml
KUEUE_CONFIG:
  default:
    queueName: "skaha-queue"
    priorityClass: "low"
  notebook:
    queueName: "skaha-gpu-queue"
    priorityClass: "high"
  carta:
    queueName: "skaha--queue"
    priorityClass: "high"
```

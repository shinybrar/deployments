# Skaha Helm Chart

See the [Deployment Guide](../science-platform/README.md) for a better idea of a full system.

The Skaha Helm chart facilitates the deployment of the Skaha application within a Kubernetes cluster. This chart is designed to streamline the installation and management of Skaha, ensuring a seamless integration into your Kubernetes environment.

## Prerequisites
Before deploying the Skaha Helm chart, ensure that the following conditions are met:

- **Kubernetes Cluster**: A running Kubernetes cluster, version 1.27 or higher.
- **Helm**: Helm package manager, version 3, installed on your machine. Refer to the [official Helm documentation](https://helm.sh/docs/) for installation instructions.
- **Kueue**: Kueue must be installed in your cluster, as Skaha integrates with Kueue for job queueing. Follow the [Kueue installation guide](https://kueue.sigs.k8s.io/docs/) to set it up.

## Installation
To deploy the Skaha application using the Helm chart, follow these steps:

1. **Add the Skaha Helm Repository**:
```bash
helm repo add skaha-repo https://images.opencadc.org/chartrepo/platform
```

2. **Update Helm Repositories**:
```bash
helm repo update
```

3. **Install the Skaha Chart**:
```bash
helm install skaha-release skaha-repo/skaha
```

Replace `skaha-release` with your desired release name.

## Configuration
The Skaha Helm chart comes with a default configuration suitable for most deployments. However, you can customize the installation by providing your own `values.yaml` file. This allows you to override default settings such as resource allocations, environment variables, and other parameters.

To customize the installation:

- **Create a `values.yaml` File**: Define your custom configurations in this file.
- **Install the Chart with Custom Values**:
```bash
helm install skaha-release skaha-repo/skaha -f values.yaml
```

### Supported Configuration Options
The following table lists the configurable parameters for the Skaha Helm chart:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `kubernetesClusterDomain` | Kubernetes cluster domain used to find internal hosts | `cluster.local` |
| `replicaCount` | Number of Skaha replicas to deploy | `1` |
| `skaha.namespace` | Namespace where Skaha is deployed | `skaha-system` |
| `skahaWorkload.namespace` | Namespace where Skaha Workload (User Sesssion space) is deployed | `skaha-workload` |
| `deployment.hostname` | Hostname for the Skaha deployment | `""` |
| `deployment.skaha.image` | Skaha Docker image | `images.opencadc.org/platform/skaha:<current release version>` |
| `deployment.skaha.imagePullPolicy` | Image pull policy for the Skaha container | `IfNotPresent` |
| `deployment.skaha.imageCache.refreshSchedule` | Schedule for refreshing the Skaha image cache in `cron` format | `@daily` |
| `deployment.skaha.skahaTld` | Top-level directory for Skaha | `/cavern` |
| `deployment.skaha.defaultQuotaGB` | Default quota for Skaha in GB.  Used when allocating first-time users into the system. | `10` |
| `deployment.skaha.registryHosts` | Space delimited list of Docker (Harbor) registry hosts | `images.canfar.net` |
| `deployment.skaha.usersGroup` | GMS style Group URI for Skaha users to belong to | `""` |
| `secrets` | List of secrets to be mounted in the Skaha deployment defined as objects `secretName: {}` | `[]` |

### Integration with Kueue
Skaha leverages Kueue for efficient job queueing and management. Ensure that Kueue is properly installed and configured in your cluster. For detailed information on Kueue's features and setup, refer to the [Kueue documentation](https://kueue.sigs.k8s.io/docs/).

## Uninstallation
To remove the Skaha application from your cluster:

```bash
helm uninstall skaha-release
```

This command will delete all resources associated with the Skaha release.

## License
This project is licensed under the MIT License. For more information, refer to the LICENSE file in the repository.

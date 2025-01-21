# Developer Guide for Kueue

## Install Kube-Prometheus Stack

Before you install, `kueue` on Docker Desktop Kubernetes, you need to install the `kube-prometheus` stack. The `kube-prometheus` stack is a collection of Kubernetes manifests, Grafana dashboards, and Prometheus rules combined with Helm charts to provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus using the Prometheus Operator.

The Prometheus Operator is required for exporting kueue metrics. This is controlled by the following configuration in the `values.yaml` file:
  ```
  enablePrometheus: true
  ```

To install the `kube-prometheus` stack on Docker Desktop Kubernetes, you can use the following steps:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack
```

### Patch for `node-exporter` DaemonSet on Docker Desktop Kubernetes

```bash
kubectl patch ds monitoring-prometheus-node-exporter --type "json" -p '[{"op": "remove", "path" : "/spec/template/spec/containers/0/volumeMounts/2/mountPropagation"}]'
```

### Access Monitoring Stack

#### Grafana Credentials
```bash
echo "Username: admin"
echo "Password: $(kubectl get secret monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode)"
```

#### Port Forwarding

```bash
kubectl port-forward svc/monitoring-grafana 3000:80
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Visit, [http://localhost:3000](http://localhost:3000) and login with the above credentials.

## Kueue Installation

```bash
git clone http://github.com/kubernetes-sigs/kueue.git
git clone http://github.come/opencadc/deployments.git

cd kueue/charts/kueue
helm install kueue -n default -f ../../deployments/configs/kueue/dev.values.yaml .
```
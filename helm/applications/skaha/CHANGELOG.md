# CHANGELOG for Skaha User Session API Helm Chart

## 2025.09.29 (1.1.0)
- Bump Skaha API image to `1.1.0`
- Feature Gate to support `LimitRange` objects to enforce resource limits on User Sessions

## 2025.09.29 (1.0.5)
- Fix for status reporting in User Sessions

## 2025.09.11 (1.0.4)
- Provide Kueue examples with documentation
- Fix typo in headless priority class name setting
- Fix environment variable name to properly be uppercase for headless priority class
- Bump Skaha API image to `1.0.3`

## 2025.09.10 (1.0.3)
- Fix to display GPU Cores

## 2025.09.10 (1.0.2)
- Remove Firefly `readinessProbe` to investigate timeouts

## 2025.09.10 (1.0.1)
- Fix NPE when launching Desktop App
- Fix for Job listing omitting Jobs with a failed Pod, but Active Pods are still greater than zero (0)

## 2025.09.09 (1.0.0)
- Official release
- Add CARTA 5.0
- Support for Kueue

## 2025.08.19 (0.11.23)
- Feature: API version configurable (Revert Ingress)

## 2025.08.19 (0.11.21)
- Feature: Add release name to make unique object names

## 2025.08.19 (0.11.17)
- Feature: Add support for configuring API versioning.

## 2025.08.01 (0.11.16)
- Fix: Connection leaks detected from repeated Redis access.  Blocked those up.

## 2025.07.15 (0.11.15)
- Feature: Set the default memory consumption to 1Gi.

## 2025.07.11 (0.11.14)
- Feature: Set the default resource consumption request (RAM and CPU Cores) for User Sessions when none are specified.
- Feature: Bump Skaha API image to `0.29.1`.

## 2025.07.10 (0.11.13)
- Feature: Add support for TLS in User Sessions IngressRoute.

## 2025.07.09 (0.11.12)
- Fix: Remove unnecessary missing label messager from image caching script.
- Feature: Make `imagePullPolicy` configurable for User Sessions.

## 2025.06.10 (0.11.10)
- Fix: Do not assume separate Namespaces for the User Sessions and Skaha API.  The Workload Namespace defaults to `skaha-workload`, but will use the same as the Skaha API if empty.

## 2025.05.08 (0.11.9)
- Update image version to reflect Firefly changes

## 2025.05.08 (0.11.8)
- Add Firefly backend type to Skaha API

## 2025.05.08 (0.11.7)
- Fix for Redis image setting for initContainers.

## 2025.04.15 (0.11.4)
- Add `tolerations` feature for `skaha` API and User Sessions.
  - See https://github.com/opencadc/deployments/issues/29

## 2025.04.10 (0.11.3)
- Fix for multiple Harbor repository hosts (`registryHosts` variable)

## 2025.03.14 (0.11.2)
- Fix for how Skaha queries for `LocalQueue` objects.

## 2025.03.11 (0.11.0)
- Configure queueing system via Kueue.

## 2025.02.06 (0.10.3)
- Omit image pull secrets (`imagePullSecrets`) from `Job` launch when not used.

## 2025.02.03 (0.10.2)
- Fix missing swagger documentation
- Fix Desktop menu building

## 2025.01.22 (0.10.0)
- Allow specific hostname for user sessions
- Code cleanup

## 2025.01.17 (0.9.5)
- Use new Traefik API Group (traefik.io) (https://doc.traefik.io/traefik/v2.10/migration/v2/#kubernetes-crds)

## 2024.10.23 (0.9.0)
- Add `x-skaha-registry-auth` request header support to set Harbor CLI secret (or other Image Registry secret)

## 2024.10.18 (0.8.0)
- Allow setting nodeAffinity values for proper scheduling.

## 2024.10.10 (0.7.8)
- Fix for client certificate injection

## 2024.10.07 (0.7.3)
- Fix for security context in image caching job

## 2024.10.04 (0.7.2)
- Fix to inject user client certificates properly

## 2024.10.03 (0.7.1)
- Small fix to ensure userinfo endpoint is obtained from the Identity Provider for applications using the StandardIdentityManager

## 2024.09.20 (0.6.0)
- Feature to allow mounting volumes into user sessions

## 2024.09.19 (0.5.1)
- Fix to add `headlessPriorityGroup` and `headlessPriorityClass` configurations

## 2024.09.10
- Enforce configuration by deployers by removing some default values
- Sessions now contain their own stanza (`sessions:`)
  - `deployment.skaha.maxUserSessions` is now `deployment.skaha.sessions.maxCount`
  - `deployment.skaha.sessionExpiry` is now `deployment.skaha.sessions.expirySeconds`
  - Added `deployment.skaha.sessions.minEphemeralStorage` and `deployment.skaha.sessions.maxEphemeralStorage`

## 2024.09.04
- Fix for Desktop Applications not starting due to API token being overwritten

## 2024.05.06
- Small change to deploy on CADC infrastructure with CephFS quotas

## 2024.03.11
- Large development branch merged into `master`.  This is a point release only.

## 2024.02.26
- Fix multiple users in Desktop session Applications
- Add `loggingGroup` access to permit log level modification
- Externalize the CARTA startup script to better diagnose issues
- Bug fixes around user home directory allocations

## 2024.01.12 (0.3.6)
- Desktop sessions have trusted API access to the Skaha service
- Better support for Access Tokens

## 2023.11.14 (0.3.0)
- Desktop sessions are still not complete, but have improved.
  - Fix to call menu building using Tokens
  - Fix Desktop and Desktop App launching to use Tokens for authenciated access back to Skaha
- Fix PosixPrincipal username if missing

## 2023.11.02 (0.2.17)
- Remove unnecessary call to POSIX Mapper for Group mapping (Bug - performance)
- Fix when POSIX Mapper includes large number of users and/or groups (Bug)
- Clean up of code

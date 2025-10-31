# CHANGELOG for Cavern User Storage Helm Chart

## 2025.09.22 (0.7.1)
- Make liveness and readiness probes configurable.

## 2025.09.09 (0.7.0)
- Feature: Support `admin-api-key` (`.deployment.cavern.adminAPIKeys`) for trusted admin access.

## 2025.08.21 (0.6.7)
- Fix: Wee regression with the JWSK feature.

## 2025.07.29 (0.6.6)
- Fix: `NullPointerException` in `cavern` service.
- Feature: Add JWSK (JWT Set Key) support for OIDC authentication.

## 2025.06.17 (0.6.5)
- Small feature to allow user allocation on behalf of another user's JWT.  This is support for the OIDC scenario.

## 2025.05.07 (0.6.4)
- Update to `cavern` 0.8.1 image.
- Added `deployment.cavern.uws.db.image` to specify PostgreSQL image.

## 2025.04.15 (0.6.1)
- Add `tolerations` feature for `cavern` API and supprting PostgreSQL deployment.
  - See https://github.com/opencadc/deployments/issues/29

## 2025.01.09 (0.6.0)
- Small fix to remove unnecessary init container for Cavern
- Small fix to remove public access to /home folder (`cavern` 0.8.0)

## 2024.10.08
- Update to omit PostgreSQL in favour of an existing database.

## 2024.10.03 (0.4.7)
- Small bug fix to properly ask the OIDC Discovery document for the userinfo endpoint.

## 2024.09.18 (0.4.6)
- Bug fix for setting quotas

## 2024.09.13 (0.4.5)
- Bug fix for database initialization

## 2024.05.27 (0.4.0)
- Enforcing some values to be set by the deployer.
- Fix for Quota reporting
- Fix for folder size reporting
- Added `extraHosts` mapping for manual DNS entries
- Added `extraConfigData` to add to the Cavern `ConfigMap`.

## 2024.03.12 (0.3.0)
- Bug fixes in allocation
- Bug fixes in read permission with sub-paths

## 2023.11.29 (0.2.0)
- Fix to support creating links in the User Interface properly
- Support for pre-authorized URL key generation
- Added `applicationName` configuration to rename the underlying WAR file to serve from another endpoint
- Code cleanup

# Storage User Interface Helm Chart (0.4.0)

## December 11, 2024 (0.4.0)
- Added support for `securityContext`
- Added support to rename application to change endpoint (`applicationName`)

## December 3, 2024 (0.3.0)
* Add batch download options
* Small optimizations and fixes

## June 24, 2024 (0.2.3)
* Fix to use tokens for APIs on a different host.

## April 5, 2024 (0.1.7)
* Add feature to set Kubernetes secret to declare OpenID Connect client secret to avoid setting it explicitly

## January 12, 2024 (0.1.3)
* OpenID Connect compliant with Authorization Code flow
* Feature flag to disable some features (Batch download/upload, ZIP Download, Create External Links, Supports Paginated downloads)
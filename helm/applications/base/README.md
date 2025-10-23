# base

![Version: 0.4.1](https://img.shields.io/badge/Version-0.4.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.4](https://img.shields.io/badge/AppVersion-0.1.4-informational?style=flat-square)

A Helm chart to install base components of the CANFAR Science Platform

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Shiny Brar | <shiny.brar@nrc-cnrc.gc.ca> |  |
| Dustin Jenkins | <djenkins.cadc@gmail.com> |  |

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://traefik.github.io/charts | traefik | 37.2.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| kubernetesClusterDomain | string | `"cluster.local"` |  |
| secrets | string | `nil` |  |
| skaha.namespace | string | `"skaha-system"` |  |
| skahaWorkload.namespace | string | `"skaha-workload"` |  |
| traefik.install | bool | `false` |  |
| traefik.logs.access.enabled | bool | `false` | To enable access logs |
| traefik.logs.general.level | string | `"ERROR"` | Alternative logging levels are DEBUG, PANIC, FATAL, ERROR, WARN, and INFO. |

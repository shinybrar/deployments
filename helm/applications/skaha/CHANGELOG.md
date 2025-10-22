# CHANGELOG for Skaha User Session API (Chart 1.1.0)

## [1.1.0](https://github.com/shinybrar/deployments/compare/skaha-1.0.4...skaha-1.1.0) (2025-10-22)


### Features

* add ability to set hostname to deploy user sessions on separate host ([7ae003b](https://github.com/shinybrar/deployments/commit/7ae003b1f587aa288da6c8647de47be6477d3eef))
* add ability to set hostname to deploy user sessions on separate… ([8ff451a](https://github.com/shinybrar/deployments/commit/8ff451ae2ae44c1d66c6938cfec373ed19b0692a))
* add hostname for sessions and base chart ([4e58f21](https://github.com/shinybrar/deployments/commit/4e58f21a26965cd6847da8c06caa258049715f72))
* add kueue as dependency to skaha chart ([970762e](https://github.com/shinybrar/deployments/commit/970762ecaa1e3a87891ed8834b7eaf5d92e08847))
* add limit range configuration and update docs ([4eaf993](https://github.com/shinybrar/deployments/commit/4eaf993b33da03033d6fa83638791fea61d3b088))
* add limit range object ([1219c78](https://github.com/shinybrar/deployments/commit/1219c78f9bac27c41d11082e89a96bfb6ca8a515))
* add setting queue per session ([57cb88b](https://github.com/shinybrar/deployments/commit/57cb88baac33cf5fb739c2579757abc28db4f54f))
* add skaha helm chart ([fea49a4](https://github.com/shinybrar/deployments/commit/fea49a4777d77ecc4d8e756fa5dc2be63d5ae0d1))
* add skaha helm chart ([75904dc](https://github.com/shinybrar/deployments/commit/75904dce06b11de8350b24e3b9a8a49102f25b36))
* add tls yaml support for configuration of user session ingress ([d9cfe73](https://github.com/shinybrar/deployments/commit/d9cfe7364652f241254bc3c490e7c59b58de16ff))
* add tls yaml support for configuration of user session ingressroutes ([fdb924e](https://github.com/shinybrar/deployments/commit/fdb924e31a8e1c808d92017bc670eae7984b5dc3))
* add tolerations to apis and uis to allow fine grained node deployment ([a2ba229](https://github.com/shinybrar/deployments/commit/a2ba2291ffc4cbb41cf47b0d6f1376c8ec64d3d7))
* added kueue documentation and renamed skaha property ([5feca3a](https://github.com/shinybrar/deployments/commit/5feca3ada2e3938cca2247f374a64f0c04266710))
* allow setting images for those defaulting to docker io ([da0d2e7](https://github.com/shinybrar/deployments/commit/da0d2e7fbcf90639adc83a47b0517de827929399))
* allow setting images for those defaulting to docker io ([97574c2](https://github.com/shinybrar/deployments/commit/97574c274c1bf459951d21edbcf539a0abfe0398))
* backward compat for carta ([228cea7](https://github.com/shinybrar/deployments/commit/228cea7754fb7552b19d4a5d0d68696d9eb2cb6c))
* carta 5 support and enable compression and remove port spec ([789e40e](https://github.com/shinybrar/deployments/commit/789e40e87e860e35dcfbc2bf5db1532ae6d82c7a))
* **helm-docs:** migrated existing readme to docs, and auto-generated new chart readme, based on values.yml files ([fc2311f](https://github.com/shinybrar/deployments/commit/fc2311f11767056b3cc612f45af6e1e87e470ea3))
* kueue dependency and documentation ([e4da605](https://github.com/shinybrar/deployments/commit/e4da6052bcdbc87be14d4c4205f05302256cf363))
* make api version configurable ([ff4c4ed](https://github.com/shinybrar/deployments/commit/ff4c4ed478fd31dc5ab6e35e00f4f4e6077537c2))
* make api version configurable ([a2ed96a](https://github.com/shinybrar/deployments/commit/a2ed96a5ad7d79931e228b6fc820526b32a27984))
* make exposed port configurable ([75ff51d](https://github.com/shinybrar/deployments/commit/75ff51dfc897a28ba345d4850080a1689fed8ba1))
* make image pull policy for user sessions configurable ([36d3fe9](https://github.com/shinybrar/deployments/commit/36d3fe9349b077f75876c59aa1ac1065a93cc37d))
* make image pull policy for user sessions configurable ([d700606](https://github.com/shinybrar/deployments/commit/d7006062a0adab681f218580229579789d5d5565))
* manage limitrange objects for experimental feature gate ([60dd99c](https://github.com/shinybrar/deployments/commit/60dd99cc0520abd08fe8dc6c6adbb905e554cf20))
* merge main and clean up kueue configuration ([6231184](https://github.com/shinybrar/deployments/commit/6231184718738cf21cdcbfa7bf722adccef07c7a))
* **skaha:** added firefly svc and launch manifest for k8s ([1e976e4](https://github.com/shinybrar/deployments/commit/1e976e4bdce4876216e5dab28424caca7b7cf29a))
* **skaha:** added ingress config for firefly sessions ([dd828a3](https://github.com/shinybrar/deployments/commit/dd828a3769555bf3b67f93dfc4ce8e7dbc55492c))
* version bump for new image to declare default resource values w… ([9a199f8](https://github.com/shinybrar/deployments/commit/9a199f8c85d3e1f8d3e8282a9f831b30ede92182))
* version bump for new image to declare default resource values when none specified ([92c477a](https://github.com/shinybrar/deployments/commit/92c477ae26a56fd11e3e39500871076fa3efcb1b))


### Bug Fixes

* add api version configuration for deployment ([3e28a77](https://github.com/shinybrar/deployments/commit/3e28a771387c645402a9b84c75741d183b806a1a))
* add owner references to ensure objects are cleaned up after jobs are deleted ([71f0b4e](https://github.com/shinybrar/deployments/commit/71f0b4ea17548c9d935feab76567f7abdb7ea576))
* add redis updates for cve fix and skaha limit range object ([e8c02c0](https://github.com/shinybrar/deployments/commit/e8c02c0e780d7eeebceed6c237e409d5fc84dba5))
* add release name to image cache job ([3dd45fe](https://github.com/shinybrar/deployments/commit/3dd45fef9f52e37e9b350b1b498133c9671e8fc6))
* added appid label to copy ([c88698b](https://github.com/shinybrar/deployments/commit/c88698b5f220024b39777c52b7a4c1ae76cff4d0))
* added helpful message ([8158cbf](https://github.com/shinybrar/deployments/commit/8158cbf79c2e5187c7f2d091164dc60d3537af9b))
* alter default cron frequency and update image version ([afebd51](https://github.com/shinybrar/deployments/commit/afebd5102fe549aeb67f394c951d2aa389acd307))
* bump image version ([5bc209b](https://github.com/shinybrar/deployments/commit/5bc209bfa64b449fcea0fb9f8b6ee76504bd16d9))
* changelog 1_0 change ([0fdf87c](https://github.com/shinybrar/deployments/commit/0fdf87c093756412de1c99db059906b68523595a))
* configure workload pvc name and remove kueue annotations ([af0803a](https://github.com/shinybrar/deployments/commit/af0803a04ff5ad59642423c9ec54265d51c4d69b))
* configure workload pvc name and remove kueue annotations ([304863d](https://github.com/shinybrar/deployments/commit/304863dd53823280ad49448876c1e451196d7de1))
* controller to false for desktop apps to be allowed into kueue ([26af9f3](https://github.com/shinybrar/deployments/commit/26af9f355890c5cec77ed6ec2266dbbcefb641a3))
* corrected default skaha image ([7e3fe53](https://github.com/shinybrar/deployments/commit/7e3fe536e0933bc15ef4beb08522974262bffc10))
* debug redis puts ([81e36a8](https://github.com/shinybrar/deployments/commit/81e36a8e70ae8b7a2eae11615b1f00f7f71a4a01))
* **desktop:** removed +x from all desktop configuration templates ([26e11cf](https://github.com/shinybrar/deployments/commit/26e11cf7270a89b2e8c759458ef117de62069f9f))
* ensure release name is consistent ([6391e2e](https://github.com/shinybrar/deployments/commit/6391e2ea1a0be97628076c18474160e154e91580))
* **firefly:** mem request ([eac4bba](https://github.com/shinybrar/deployments/commit/eac4bbad0b922d00c89960950b6642a1dfabc96f))
* **firefly:** removed error in spec.container.env ([ee32518](https://github.com/shinybrar/deployments/commit/ee32518c7822ba497c4f1b0864d10950050d9b4f))
* **firefly:** removed jupyter configmap, cleaned up cmd args ([af2b2f4](https://github.com/shinybrar/deployments/commit/af2b2f48de43b81a27f132ea128542d6555eebc2))
* fix connection leaks from redis ([7c91e78](https://github.com/shinybrar/deployments/commit/7c91e7894040bad2d9d532f9301b07a3471c302a))
* fix connection leaks from redis ([db1e70e](https://github.com/shinybrar/deployments/commit/db1e70eeccd1acdd4d4e748f04e24b975357f91e))
* fix for default limit values ([c8bdebb](https://github.com/shinybrar/deployments/commit/c8bdebb9c4a889e8b8c835298d2b8479d8f8521f))
* fix for helm versions ([543bd8e](https://github.com/shinybrar/deployments/commit/543bd8ee065b4ed07c37108c2efdc0faf54babbb))
* fix for kueue install order fix ([d2a2b97](https://github.com/shinybrar/deployments/commit/d2a2b9767261f7ace335acab601f5712ebf97db9))
* fix for pvc name ([e3e5f5b](https://github.com/shinybrar/deployments/commit/e3e5f5bb88320aefb2b4c53033b0458372e113f4))
* fix for redis image used in initcontainers ([0ef9e32](https://github.com/shinybrar/deployments/commit/0ef9e3244e48afd85ffd22a50395b0a1229a9b29))
* fix for redis image used in initcontainers ([76765c6](https://github.com/shinybrar/deployments/commit/76765c62f605249acd0630a81b18a943447518d8))
* fix for values location for storage pvc ([2d68b31](https://github.com/shinybrar/deployments/commit/2d68b31526141d0158ca25a65962b2afeeb09149))
* fix for values reference ([fe5f54d](https://github.com/shinybrar/deployments/commit/fe5f54dec16738484e82c23976d2e3c6528988ea))
* fix for values reference ([8674928](https://github.com/shinybrar/deployments/commit/86749289165ca9da28a1d2b27b9e8720bed1e8b5))
* fix gpu cores display ([d207c1b](https://github.com/shinybrar/deployments/commit/d207c1b0503547331f8f13e4b60e7030866809bf))
* fix hostname setting for desktop ([38ba33c](https://github.com/shinybrar/deployments/commit/38ba33c525bde5fabad9c344d0aaa31413c2553e))
* fix middleware name ([27d2fc8](https://github.com/shinybrar/deployments/commit/27d2fc81e0d3b5987dbf8f2ccfa401d5c75523b9))
* fix release name changes ([df94c4d](https://github.com/shinybrar/deployments/commit/df94c4dfc52938d83008be174ffd85c11dd10e19))
* fix volume mount names ([85dd2ff](https://github.com/shinybrar/deployments/commit/85dd2ffe0f3eb5896bf3025e941890b8f5cd0437))
* for for adding cred to regitry client ([68a280a](https://github.com/shinybrar/deployments/commit/68a280ad8d98a2f339f377c0a48d721b600d5f3c))
* for for adding cred to regitry client ([6e53a43](https://github.com/shinybrar/deployments/commit/6e53a436f255201ceee85cc9475f4af21c7f730e))
* handle gpu limits properly ([cb6c2fe](https://github.com/shinybrar/deployments/commit/cb6c2fe299235ded182337f43597e5bf9027f326))
* **helm:** maintainer updates ([6af7785](https://github.com/shinybrar/deployments/commit/6af7785e0b840d4b58224f114caa20ef255cd473))
* **helm:** skaha chart cavern-volume is now a required field ([8a4c33d](https://github.com/shinybrar/deployments/commit/8a4c33dc0ed6f5c3cbd2c4234b4bec24920bc72e))
* **helm:** skaha resources now have valid json format ([90adb97](https://github.com/shinybrar/deployments/commit/90adb9725de3fecc0eb0303631e5f8b437755fa3))
* **helm:** updated maintainers ([67803b1](https://github.com/shinybrar/deployments/commit/67803b18ec5e2762f0942451894e4c9b8c7ee2f9))
* image pull secret is omitted by default ([39cd8e3](https://github.com/shinybrar/deployments/commit/39cd8e3ba95d21f69ec99e9941e656ef82b9ca47))
* image pull secret is omitted by default ([b14479d](https://github.com/shinybrar/deployments/commit/b14479d4d48eb19472b3d3220166042f5151648f))
* image version fix ([2bcabae](https://github.com/shinybrar/deployments/commit/2bcabae1144f7c854e77e05e6275a872cda770c1))
* include ownserhip in desktop apps to be cleaned up if desktop removed ([65317d8](https://github.com/shinybrar/deployments/commit/65317d83b9ecb9416a93c6498e0b62c1700cdfe3))
* kueue lookup fix ([bc2661c](https://github.com/shinybrar/deployments/commit/bc2661c185d39c18d53d41ecb50aeeb07c16215b))
* kueue lookup fix ([c9fba56](https://github.com/shinybrar/deployments/commit/c9fba56c567d3e614db873ff31b5ef39cec4e038))
* **maintainers:** now need atleast 15 commits in the last 12 months to be considered a maintainer ([02954e4](https://github.com/shinybrar/deployments/commit/02954e4e190774cf4756e9b3f90594eac2a80499))
* make ingress path configurable ([28599f3](https://github.com/shinybrar/deployments/commit/28599f3d1e4702558eb373a2927411e3aaf14b6e))
* new chart to fix harbor hosts setting ([e9af721](https://github.com/shinybrar/deployments/commit/e9af7212e774232a5226df433d46dfcaec8ea264))
* new chart to fix harbor hosts setting ([16aef98](https://github.com/shinybrar/deployments/commit/16aef988cdbd7e34071dda4256abc1c50548fa3d))
* **pre-commit:** added auto-generated helm-maintainers section to all helm charts ([882dfb9](https://github.com/shinybrar/deployments/commit/882dfb9f2cf2f0d1b3615d7768b92a2f39c122b8))
* **pre-commit:** end-of-file-fixer ([1d658c7](https://github.com/shinybrar/deployments/commit/1d658c75c74faedd7293d5151be51df295a1ddd9))
* **pre-commit:** trailing-whitespaces ([178468c](https://github.com/shinybrar/deployments/commit/178468c8082ca69a395ebc5e185a2186afbb3335))
* prepend release for middlewrae ([3d35513](https://github.com/shinybrar/deployments/commit/3d35513aa77a441cfeed3931429335e1c6d4bec7))
* prepend with release name ([74f14e9](https://github.com/shinybrar/deployments/commit/74f14e94f9cf965f0bb128e62710d5c2a32e7001))
* proper env name ([e12e8a6](https://github.com/shinybrar/deployments/commit/e12e8a65288f3eedc941184a5a4bdcae7ff93c51))
* proper middleware name and probe removal ([4c569b9](https://github.com/shinybrar/deployments/commit/4c569b92a86347e4a28727c8fe447f167181848d))
* proper middleware name and probe removal ([6d7df74](https://github.com/shinybrar/deployments/commit/6d7df74d168fbc93a0b5a9aa558d2d32b218837d))
* remove api version from ingress ([1502f1f](https://github.com/shinybrar/deployments/commit/1502f1f506af5747563974b44e0786ba2bf51eb9))
* remove kueue chart dependency ([a57e38f](https://github.com/shinybrar/deployments/commit/a57e38fb95e2dfa9c25103700512965804d4ef71))
* remove misleading error message in image cache script ([a727d9c](https://github.com/shinybrar/deployments/commit/a727d9ce2b6494fa3134dff26c7d287de65960d7))
* remove whitespace ([e06ad8b](https://github.com/shinybrar/deployments/commit/e06ad8b0bf13d0f6bb950ccd721f7dbbeb5492d9))
* remove ws endpoint to single endpoint and readd port spec ([76a3f03](https://github.com/shinybrar/deployments/commit/76a3f03d1efc5db63159b97da9bdb7e0917708b0))
* **skaha:** added bash shebang for cache-images script ([d19ba62](https://github.com/shinybrar/deployments/commit/d19ba625bd22acc65255810cb427c946ea933a74))
* small fix for object names ([4787817](https://github.com/shinybrar/deployments/commit/47878179daf9bd7a71b044e2e551aa4ef9769148))
* swagger doc fix in skaha ([f240a85](https://github.com/shinybrar/deployments/commit/f240a852958abf764a447895864df523b2b06258))
* swagger doc fix in skaha ([921df0a](https://github.com/shinybrar/deployments/commit/921df0aff35ebd5e0239fe4fd7b074af70d272be))
* unique names for objects using release name ([28e014f](https://github.com/shinybrar/deployments/commit/28e014ff9d2b8f8c1a18e23dbbc4357a7c901301))
* unique names for objects using release name ([ee8dbcf](https://github.com/shinybrar/deployments/commit/ee8dbcf864771a34ed6916e4a02aa45d9ea69ca0))
* update version ([911f90e](https://github.com/shinybrar/deployments/commit/911f90e43b78726b3d35dbc2d70c843f25e819fb))
* update version ([708fbd2](https://github.com/shinybrar/deployments/commit/708fbd2ba07c2cb59d0ddfe13432bc1957801e19))
* update version to match new image ([fe9a43a](https://github.com/shinybrar/deployments/commit/fe9a43a2fe39acc96cee2a10d755afa3e8b6eb92))
* update version to match new image ([798bad3](https://github.com/shinybrar/deployments/commit/798bad3e3f5f1da22aa8a37ee5e764a8b8f3a461))
* update versions ([c7d4710](https://github.com/shinybrar/deployments/commit/c7d4710dd2167f513640bcc98476428327ad7d04))
* use latest traefik api group ([a776214](https://github.com/shinybrar/deployments/commit/a776214ae68a91a3dab99d67608972558a21b247))
* use latest traefik api group ([84debe4](https://github.com/shinybrar/deployments/commit/84debe45777162ae258acb51ab05c60c8d8617e5))
* use staged images to avoid docker io repository rate limits ([48325f8](https://github.com/shinybrar/deployments/commit/48325f87198281b97372b0000c8eb277530460a6))
* use staged images to avoid docker io repository rate limits ([8a12285](https://github.com/shinybrar/deployments/commit/8a122853ed1917cc3679ce9655ea8ffbe8dba320))
* version chore ([4dda080](https://github.com/shinybrar/deployments/commit/4dda0803b7d2d9e657682dbb1b8dc4ccd9aba482))
* version chore ([e3347f7](https://github.com/shinybrar/deployments/commit/e3347f7b8e34de0a22884ca4b64c349e7df62704))
* version update ([b8025c2](https://github.com/shinybrar/deployments/commit/b8025c241cc22585eceb0e9808e44c0e17f52ce3))

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

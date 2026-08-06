# kusai-mastodon

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.3.1](https://img.shields.io/badge/AppVersion-0.3.1-informational?style=flat-square)

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| kasefuchs | <kasefuchs@protonmail.com> |  |

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://bjw-s-labs.github.io/helm-charts | common | 5.0.1 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config | object | `{}` |  |
| configMaps.config.data."config.yaml" | string | `"{{- with .Values.config }}\n{{- toYaml . | nindent 8 }}\n{{- end }}"` |  |
| controllers.post.containers.main.<<.env.KUSAI_MASTODON_STATE_PATH | string | `"/app/data/state.json"` |  |
| controllers.post.containers.main.<<.image.repository | string | `"codeberg.org/kasefuchs/extra/kusai-mastodon"` |  |
| controllers.post.containers.main.<<.image.tag | string | `nil` |  |
| controllers.post.containers.main.<<.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| controllers.post.containers.main.<<.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| controllers.post.containers.main.<<.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| controllers.post.containers.main.<<.securityContext.runAsGroup | int | `1000` |  |
| controllers.post.containers.main.<<.securityContext.runAsNonRoot | bool | `true` |  |
| controllers.post.containers.main.<<.securityContext.runAsUser | int | `1000` |  |
| controllers.post.containers.main.args[0] | string | `"--config-path"` |  |
| controllers.post.containers.main.args[1] | string | `"/app/config/config.yaml"` |  |
| controllers.post.containers.main.args[2] | string | `"post"` |  |
| controllers.post.cronjob.failedJobsHistory | int | `3` |  |
| controllers.post.cronjob.schedule | string | `"0 * * * *"` |  |
| controllers.post.cronjob.successfulJobsHistory | int | `1` |  |
| controllers.post.pod.securityContext.fsGroup | int | `1000` |  |
| controllers.post.pod.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| controllers.post.pod.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| controllers.post.type | string | `"cronjob"` |  |
| controllers.reply.containers.main.<<.env.KUSAI_MASTODON_STATE_PATH | string | `"/app/data/state.json"` |  |
| controllers.reply.containers.main.<<.image.repository | string | `"codeberg.org/kasefuchs/extra/kusai-mastodon"` |  |
| controllers.reply.containers.main.<<.image.tag | string | `nil` |  |
| controllers.reply.containers.main.<<.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| controllers.reply.containers.main.<<.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| controllers.reply.containers.main.<<.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| controllers.reply.containers.main.<<.securityContext.runAsGroup | int | `1000` |  |
| controllers.reply.containers.main.<<.securityContext.runAsNonRoot | bool | `true` |  |
| controllers.reply.containers.main.<<.securityContext.runAsUser | int | `1000` |  |
| controllers.reply.containers.main.args[0] | string | `"--config-path"` |  |
| controllers.reply.containers.main.args[1] | string | `"/app/config/config.yaml"` |  |
| controllers.reply.containers.main.args[2] | string | `"reply"` |  |
| controllers.reply.cronjob.failedJobsHistory | int | `3` |  |
| controllers.reply.cronjob.schedule | string | `"*/10 * * * *"` |  |
| controllers.reply.cronjob.successfulJobsHistory | int | `1` |  |
| controllers.reply.pod.securityContext.fsGroup | int | `1000` |  |
| controllers.reply.pod.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| controllers.reply.pod.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| controllers.reply.type | string | `"cronjob"` |  |
| controllers.train.containers.main.<<.env.KUSAI_MASTODON_STATE_PATH | string | `"/app/data/state.json"` |  |
| controllers.train.containers.main.<<.image.repository | string | `"codeberg.org/kasefuchs/extra/kusai-mastodon"` |  |
| controllers.train.containers.main.<<.image.tag | string | `nil` |  |
| controllers.train.containers.main.<<.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| controllers.train.containers.main.<<.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| controllers.train.containers.main.<<.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| controllers.train.containers.main.<<.securityContext.runAsGroup | int | `1000` |  |
| controllers.train.containers.main.<<.securityContext.runAsNonRoot | bool | `true` |  |
| controllers.train.containers.main.<<.securityContext.runAsUser | int | `1000` |  |
| controllers.train.containers.main.args[0] | string | `"--config-path"` |  |
| controllers.train.containers.main.args[1] | string | `"/app/config/config.yaml"` |  |
| controllers.train.containers.main.args[2] | string | `"train"` |  |
| controllers.train.cronjob.failedJobsHistory | int | `3` |  |
| controllers.train.cronjob.schedule | string | `"0 3 * * *"` |  |
| controllers.train.cronjob.successfulJobsHistory | int | `1` |  |
| controllers.train.pod.securityContext.fsGroup | int | `1000` |  |
| controllers.train.pod.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| controllers.train.pod.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| controllers.train.type | string | `"cronjob"` |  |
| global.alwaysAppendIdentifierToResourceName | bool | `true` |  |
| persistence.config.globalMounts[0].path | string | `"/app/config/"` |  |
| persistence.config.identifier | string | `"config"` |  |
| persistence.config.type | string | `"configMap"` |  |
| persistence.data.accessMode | string | `"ReadWriteOnce"` |  |
| persistence.data.globalMounts[0].path | string | `"/app/data/"` |  |
| persistence.data.size | string | `"1Gi"` |  |
| persistence.data.type | string | `"persistentVolumeClaim"` |  |
| persistence.tmp.globalMounts[0].path | string | `"/tmp/"` |  |
| persistence.tmp.type | string | `"emptyDir"` |  |
| x-container.env.KUSAI_MASTODON_STATE_PATH | string | `"/app/data/state.json"` |  |
| x-container.image.repository | string | `"codeberg.org/kasefuchs/extra/kusai-mastodon"` |  |
| x-container.image.tag | string | `nil` |  |
| x-container.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| x-container.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| x-container.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| x-container.securityContext.runAsGroup | int | `1000` |  |
| x-container.securityContext.runAsNonRoot | bool | `true` |  |
| x-container.securityContext.runAsUser | int | `1000` |  |
| x-pod.securityContext.fsGroup | int | `1000` |  |
| x-pod.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| x-pod.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)

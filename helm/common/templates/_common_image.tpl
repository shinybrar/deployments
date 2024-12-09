{{/*
Assemble the image name with the registry, repository, tag and digest.
{{ include "common.image" ( dict "imageObject" .Values.path.to.the.imag ) }}
*/}}
{{- define "common.image" -}}
{{- $registryName := .imageObject.registry | required "image.registry is required." -}}
{{- $repositoryName := .imageObject.repository | required "image.repository path is required" -}}
{{- $separator := ":" -}}
{{- $termination := .imageObject.tag | toString -}}

{{- if not .imageObject.tag }}
  {{- $termination = "SNAPSHOT" -}}
{{- end -}}
{{- if .imageObject.digest }}
    {{- $separator = "@" -}}
    {{- $termination = .imageObject.digest | toString -}}
{{- end -}}
{{- if $registryName }}
    {{- printf "%s/%s%s%s" $registryName $repositoryName $separator $termination -}}
{{- else -}}
    {{- printf "%s%s%s"  $repositoryName $separator $termination -}}
{{- end -}}
{{- end -}}

#!/bin/bash

echo "Running Renovate Entrypoint Script"

# uv comes pre-installed on the renovate:full image
# Install Helm Docs
echo "Installing Helm Docs"
go install github.com/norwoodj/helm-docs/cmd/helm-docs@latest
echo "Helm Docs Installed: $(which helm-docs): $(helm-docs --version)"

# Run renovate
renovate

echo "Renovate Run Complete"

#!/bin/bash

echo "Running Renovate Entrypoint Script"

# Install uv and sync dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run renovate
renovate

# Debugging
find / | grep "deployments"

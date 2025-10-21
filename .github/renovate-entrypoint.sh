#!/bin/bash

echo "Running Renovate Entrypoint Script"

# Install uv and sync dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

echo "Renovate Entrypoint Script Complete"

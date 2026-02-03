#!/bin/bash
# Build Lambda Layer with dependencies

set -e

LAYER_DIR="lambda_layer/python"
rm -rf lambda_layer
mkdir -p $LAYER_DIR

# Install dependencies
pip install \
    fastapi==0.109.0 \
    mangum==0.17.0 \
    pydantic>=2.7.0 \
    pydantic-settings>=2.0.0 \
    boto3==1.34.0 \
    python-multipart==0.0.6 \
    python-jose[cryptography]==3.3.0 \
    httpx==0.26.0 \
    ortools==9.8.3296 \
    pandas==2.1.4 \
    openpyxl==3.1.2 \
    -t $LAYER_DIR \
    --platform manylinux2014_x86_64 \
    --only-binary=:all: \
    --python-version 3.11

# Clean up unnecessary files
find $LAYER_DIR -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find $LAYER_DIR -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find $LAYER_DIR -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true

echo "Layer built successfully in $LAYER_DIR"

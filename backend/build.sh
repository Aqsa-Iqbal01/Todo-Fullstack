#!/bin/bash
# Custom build script for Vercel deployment

# Set environment variables
export PYTHONUNBUFFERED=1

# Install dependencies using pip instead of uv
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Dependencies installed successfully"
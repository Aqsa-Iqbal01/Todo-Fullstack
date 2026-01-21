#!/bin/bash
# Build script to copy phase-3 files to backend during Vercel deployment

echo "Copying phase-3 files to backend..."

# Create necessary directories
mkdir -p src/phase-3
mkdir -p src/phase-3/chatbot
mkdir -p src/phase-3/mcp_server
mkdir -p src/phase-3/mcp_server/tools
mkdir -p src/phase-3/config
mkdir -p src/phase-3/adapters
mkdir -p src/phase-3/services

# Copy chatbot files
cp -r ../../phase-3/chatbot/*.py src/phase-3/chatbot/ 2>/dev/null || echo "No Python files in chatbot dir"
cp -r ../../phase-3/chatbot/__pycache__ src/phase-3/chatbot/ 2>/dev/null || echo "No __pycache__ in chatbot dir (this is OK)"

# Copy mcp_server files
cp -r ../../phase-3/mcp_server/*.py src/phase-3/mcp_server/ 2>/dev/null || echo "No Python files in mcp_server dir"
cp -r ../../phase-3/mcp_server/server.py src/phase-3/mcp_server/ 2>/dev/null || echo "No server.py in mcp_server dir"

# Copy mcp_server tools
cp -r ../../phase-3/mcp_server/tools/*.py src/phase-3/mcp_server/tools/ 2>/dev/null || echo "No Python files in mcp_server/tools dir"

# Copy other necessary files
cp -r ../../phase-3/config/*.py src/phase-3/config/ 2>/dev/null || echo "No Python files in config dir"
cp -r ../../phase-3/adapters/*.py src/phase-3/adapters/ 2>/dev/null || echo "No Python files in adapters dir"
cp -r ../../phase-3/services/*.py src/phase-3/services/ 2>/dev/null || echo "No Python files in services dir"

# Copy __init__.py files to make directories proper Python packages
touch src/phase-3/__init__.py
touch src/phase-3/chatbot/__init__.py
touch src/phase-3/mcp_server/__init__.py
touch src/phase-3/mcp_server/tools/__init__.py
touch src/phase-3/config/__init__.py
touch src/phase-3/adapters/__init__.py
touch src/phase-3/services/__init__.py

echo "Phase-3 files copied successfully!"
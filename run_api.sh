#!/bin/bash
# Quick start script for running the FastAPI server locally

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -e .

# Check for config file
if [ ! -f "overleaf_config.json" ]; then
    echo "⚠️  Warning: overleaf_config.json not found"
    echo "Create it from overleaf_config.example.json or set environment variables:"
    echo "  export OVERLEAF_PROJECT_ID=your_project_id"
    echo "  export OVERLEAF_GIT_TOKEN=your_git_token"
    echo "  export API_KEY=your_secure_api_key"
    echo ""
fi

# Set default API key if not set
if [ -z "$API_KEY" ]; then
    echo "⚠️  API_KEY not set. API will run without authentication."
    echo "Set it with: export API_KEY=your_secure_key"
    echo ""
fi

# Run the server
echo "Starting FastAPI server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""
python -m uvicorn overleaf_mcp.fastapi_server:app --reload --host 0.0.0.0 --port 8000

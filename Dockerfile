FROM python:3.11-slim

# Install git (required for GitPython)
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and metadata
COPY src/ ./src/
COPY pyproject.toml .
COPY README.md .

# Install the package
RUN pip install --no-cache-dir -e .

# Create cache directory
RUN mkdir -p /app/overleaf_cache

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "overleaf_mcp.fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]

#!/usr/bin/env python3
"""
FastAPI wrapper for Overleaf MCP Server.
Exposes MCP tools as HTTP endpoints for ChatGPT integration.
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Optional
import os

from .server import execute_tool, load_config

# Create FastAPI app
app = FastAPI(
    title="Overleaf MCP API",
    description="HTTP API for Overleaf LaTeX project management",
    version="1.0.0",
)

# CORS configuration for ChatGPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
API_KEY = os.environ.get("API_KEY", "")


def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key from Authorization header."""
    if not API_KEY:
        return  # No auth required if API_KEY not set
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")
    
    token = authorization.replace("Bearer ", "")
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# Request/Response models
class ToolRequest(BaseModel):
    """Generic tool execution request."""
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResponse(BaseModel):
    """Generic tool execution response."""
    result: str
    success: bool = True


# Health check
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Overleaf MCP API"}


@app.get("/health")
async def health():
    """Detailed health check."""
    config = load_config()
    return {
        "status": "healthy",
        "projects_configured": len(config.projects),
        "default_project": config.default_project,
    }


# === CREATE OPERATIONS ===

@app.post("/projects/create", response_model=ToolResponse)
async def create_project(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Create a new Overleaf project."""
    try:
        result = await execute_tool("create_project", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/create", response_model=ToolResponse)
async def create_file(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Create a new file in a project."""
    try:
        result = await execute_tool("create_file", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# === READ OPERATIONS ===

@app.get("/projects", response_model=ToolResponse)
async def list_projects():
    """List all configured projects."""
    try:
        result = await execute_tool("list_projects", {})
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/list", response_model=ToolResponse)
async def list_files(request: ToolRequest):
    """List files in a project."""
    try:
        result = await execute_tool("list_files", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/read", response_model=ToolResponse)
async def read_file(request: ToolRequest):
    """Read a file's content."""
    try:
        result = await execute_tool("read_file", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sections/list", response_model=ToolResponse)
async def get_sections(request: ToolRequest):
    """Get sections from a LaTeX file."""
    try:
        result = await execute_tool("get_sections", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sections/read", response_model=ToolResponse)
async def get_section_content(request: ToolRequest):
    """Get content of a specific section."""
    try:
        result = await execute_tool("get_section_content", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/history", response_model=ToolResponse)
async def list_history(request: ToolRequest):
    """Get git commit history."""
    try:
        result = await execute_tool("list_history", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/diff", response_model=ToolResponse)
async def get_diff(request: ToolRequest):
    """Get git diff."""
    try:
        result = await execute_tool("get_diff", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# === UPDATE OPERATIONS ===

@app.post("/files/edit", response_model=ToolResponse)
async def edit_file(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Edit a file with surgical replacement."""
    try:
        result = await execute_tool("edit_file", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/files/rewrite", response_model=ToolResponse)
async def rewrite_file(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Rewrite entire file content."""
    try:
        result = await execute_tool("rewrite_file", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sections/update", response_model=ToolResponse)
async def update_section(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Update a specific section."""
    try:
        result = await execute_tool("update_section", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/projects/sync", response_model=ToolResponse)
async def sync_project(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Sync project with Overleaf."""
    try:
        result = await execute_tool("sync_project", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# === DELETE OPERATIONS ===

@app.post("/files/delete", response_model=ToolResponse)
async def delete_file(request: ToolRequest, _: None = Depends(verify_api_key)):
    """Delete a file from the project."""
    try:
        result = await execute_tool("delete_file", request.arguments)
        return ToolResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interfaces                          │
├─────────────────────────┬───────────────────────────────────────┤
│   ChatGPT Web Browser   │   Claude Desktop / Other MCP Clients  │
│   (Custom GPT)          │   (Native MCP Protocol)               │
└───────────┬─────────────┴──────────────┬────────────────────────┘
            │                            │
            │ HTTPS                      │ stdio
            │ (OpenAPI Actions)          │ (MCP Protocol)
            │                            │
┌───────────▼────────────────────────────▼────────────────────────┐
│                    Application Layer                             │
├──────────────────────────────┬───────────────────────────────────┤
│   FastAPI HTTP Server        │   MCP Server                      │
│   (Port 8000)                │   (stdio interface)               │
│   - REST endpoints           │   - MCP tools                     │
│   - Bearer auth              │   - Direct integration            │
│   - CORS for ChatGPT         │                                   │
└──────────────┬───────────────┴───────────────┬───────────────────┘
               │                               │
               └───────────┬───────────────────┘
                           │
                           │ Calls
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Business Logic                         │
│                   (src/overleaf_mcp/server.py)                   │
│                                                                   │
│  - execute_tool()        - Parse LaTeX sections                  │
│  - load_config()         - Git operations                        │
│  - ensure_repo()         - File validation                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ Git HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
├──────────────────────────────┬──────────────────────────────────┤
│   Overleaf Git Server        │   Local Cache                    │
│   git.overleaf.com           │   ./overleaf_cache/              │
│   - Clone/Pull/Push          │   - Git repositories             │
│   - Authentication           │   - File operations              │
└──────────────────────────────┴──────────────────────────────────┘
```

## Component Details

### 1. User Interfaces

#### ChatGPT Custom GPT
- **Protocol**: HTTPS REST API
- **Authentication**: Bearer token (API_KEY)
- **Format**: JSON requests/responses
- **Use Case**: Web-based thesis editing

#### Claude Desktop / MCP Clients
- **Protocol**: Model Context Protocol (stdio)
- **Authentication**: None (local)
- **Format**: MCP messages
- **Use Case**: Desktop AI assistant integration

### 2. Application Layer

#### FastAPI Server (`fastapi_server.py`)
```python
Responsibilities:
- HTTP endpoint routing
- Request/response serialization
- Bearer token authentication
- CORS policy enforcement
- Error handling and HTTP status codes

Endpoints:
- GET  /health              → Health check
- GET  /projects            → List projects
- POST /files/list          → List files
- POST /files/read          → Read file
- POST /files/edit          → Edit file (auth required)
- POST /sections/update     → Update section (auth required)
... and more
```

#### MCP Server (`server.py`)
```python
Responsibilities:
- MCP protocol implementation
- Tool registration and discovery
- Direct stdio communication
- Same business logic as FastAPI

Tools:
- create_project, create_file
- list_projects, list_files, read_file
- edit_file, rewrite_file, update_section
- delete_file
- get_sections, get_section_content
- list_history, get_diff, sync_project
```

### 3. Core Business Logic

#### Key Functions

**Configuration Management**
```python
load_config() → Config
  ├─ Read overleaf_config.json
  ├─ Parse environment variables
  └─ Return project configurations

get_project_config(name) → ProjectConfig
  ├─ Validate project exists
  └─ Return project details
```

**Repository Management**
```python
ensure_repo(project) → Repo
  ├─ Check if repo exists locally
  ├─ Clone if missing
  ├─ Pull latest changes
  └─ Return GitPython Repo object

validate_path(base, target) → Path
  ├─ Resolve absolute path
  ├─ Check for path traversal
  └─ Return validated path
```

**LaTeX Processing**
```python
parse_sections(content) → list[Section]
  ├─ Regex match section headers
  ├─ Extract section hierarchy
  ├─ Calculate positions
  └─ Return section metadata

get_section_by_title(content, title) → str
  ├─ Parse all sections
  ├─ Find matching title
  └─ Return section content
```

**Tool Execution**
```python
execute_tool(name, arguments) → str
  ├─ Route to appropriate handler
  ├─ Perform operation
  ├─ Git commit/push if needed
  └─ Return result message
```

### 4. External Services

#### Overleaf Git Server
```
URL: https://git.overleaf.com/{project_id}
Auth: https://git:{token}@git.overleaf.com/{project_id}

Operations:
- git clone   → Initial download
- git pull    → Sync latest changes
- git push    → Upload local changes
```

#### Local Cache
```
Location: ./overleaf_cache/{project_id}/
Structure:
  ├─ .git/              → Git metadata
  ├─ main.tex           → LaTeX files
  ├─ chapter1.tex
  ├─ references.bib
  └─ ...

Purpose:
- Fast local access
- Git operations
- Temporary workspace
```

## Data Flow

### Read Operation (e.g., "Read main.tex")

```
1. ChatGPT → POST /files/read
   {
     "arguments": {
       "file_path": "main.tex"
     }
   }

2. FastAPI → Verify API key
   ├─ Check Authorization header
   └─ Validate Bearer token

3. FastAPI → execute_tool("read_file", {...})

4. Core Logic → get_project_config()
   └─ Load configuration

5. Core Logic → ensure_repo(project)
   ├─ Check ./overleaf_cache/{project_id}/
   ├─ Clone if missing
   └─ Pull latest changes

6. Core Logic → Read file
   ├─ Validate path
   ├─ Read from local cache
   └─ Return content

7. FastAPI → Return JSON response
   {
     "result": "\\documentclass{article}...",
     "success": true
   }

8. ChatGPT → Display to user
```

### Write Operation (e.g., "Edit main.tex")

```
1. ChatGPT → POST /files/edit
   {
     "arguments": {
       "file_path": "main.tex",
       "old_string": "teh",
       "new_string": "the",
       "commit_message": "Fix typo"
     }
   }

2. FastAPI → Verify API key (required for writes)

3. FastAPI → execute_tool("edit_file", {...})

4. Core Logic → ensure_repo(project)
   └─ Pull latest changes

5. Core Logic → Edit file
   ├─ Read current content
   ├─ Verify old_string exists and is unique
   ├─ Replace old_string with new_string
   └─ Write to file

6. Core Logic → Git operations
   ├─ git add main.tex
   ├─ git commit -m "Fix typo"
   └─ git push origin main

7. Overleaf → Receive changes
   └─ Update web editor

8. FastAPI → Return success
   {
     "result": "Edited and pushed 'main.tex'",
     "success": true
   }

9. ChatGPT → Confirm to user
```

## Deployment Architecture

### Local Development

```
┌─────────────────┐
│  Developer      │
│  Machine        │
│                 │
│  ┌───────────┐  │
│  │ Python    │  │
│  │ FastAPI   │  │
│  │ :8000     │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ Git Cache │  │
│  └───────────┘  │
└─────────────────┘
        │
        │ Git HTTPS
        ▼
┌─────────────────┐
│   Overleaf      │
└─────────────────┘
```

### Production (DigitalOcean)

```
┌─────────────────────────────────────────┐
│         DigitalOcean App Platform       │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Docker Container                 │  │
│  │                                   │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Python 3.11                │  │  │
│  │  │  FastAPI + Uvicorn          │  │  │
│  │  │  Port 8000                  │  │  │
│  │  └──────────┬──────────────────┘  │  │
│  │             │                     │  │
│  │  ┌──────────▼──────────────────┐  │  │
│  │  │  /app/overleaf_cache/       │  │  │
│  │  │  (Ephemeral storage)        │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Environment Variables (Secrets)  │  │
│  │  - OVERLEAF_PROJECT_ID           │  │
│  │  - OVERLEAF_GIT_TOKEN            │  │
│  │  - API_KEY                       │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  HTTPS Load Balancer             │  │
│  │  (Automatic SSL)                 │  │
│  └───────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  │ Public URL
                  │ https://app-xxxxx.ondigitalocean.app
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│   ChatGPT      │  │   Overleaf     │
│   (HTTPS)      │  │   (Git HTTPS)  │
└────────────────┘  └────────────────┘
```

## Security Architecture

### Authentication Flow

```
┌─────────────┐
│  ChatGPT    │
└──────┬──────┘
       │
       │ 1. Request with Bearer token
       │    Authorization: Bearer abc123...
       ▼
┌─────────────────────────────┐
│  FastAPI Middleware         │
│  verify_api_key()           │
│                             │
│  ├─ Extract token           │
│  ├─ Compare with API_KEY    │
│  └─ Allow/Deny              │
└──────┬──────────────────────┘
       │
       │ 2. If valid
       ▼
┌─────────────────────────────┐
│  Endpoint Handler           │
│  (Protected operation)      │
└──────┬──────────────────────┘
       │
       │ 3. Git auth
       │    https://git:{token}@git.overleaf.com
       ▼
┌─────────────────────────────┐
│  Overleaf Git Server        │
└─────────────────────────────┘
```

### Security Layers

1. **Transport Security**
   - HTTPS only (enforced by DigitalOcean)
   - TLS 1.2+ encryption

2. **Authentication**
   - Bearer token for API access
   - Git token for Overleaf access
   - Both stored as encrypted secrets

3. **Authorization**
   - Read operations: Optional auth
   - Write operations: Required auth
   - CORS: Limited to ChatGPT domains

4. **Input Validation**
   - Path traversal prevention
   - File path validation
   - JSON schema validation

## Performance Characteristics

### Latency

```
Operation          Local    DigitalOcean
─────────────────────────────────────────
Health check       <10ms    50-100ms
List files         <50ms    100-200ms
Read file          <100ms   200-400ms
Edit file          1-2s     2-4s
(includes git push)
```

### Scalability

```
Component          Bottleneck           Solution
──────────────────────────────────────────────────
FastAPI            CPU (JSON parsing)   Scale horizontally
Git operations     Network I/O          Cache locally
Overleaf sync      Git server rate      Batch operations
Storage            Disk space           Periodic cleanup
```

### Resource Usage

```
Component          Memory    CPU       Disk
────────────────────────────────────────────
FastAPI server     50-100MB  <5%       -
Git cache          -         -         ~50MB/project
Python runtime     100MB     <10%      -
Total (1 project)  ~200MB    <15%      ~50MB
```

## Error Handling

### Error Flow

```
┌─────────────┐
│  Operation  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Try operation              │
└──────┬──────────────────────┘
       │
       ├─ Success → Return result
       │
       └─ Exception
          │
          ▼
┌─────────────────────────────┐
│  Catch and classify         │
│                             │
│  ├─ ValueError              │
│  │   → 400 Bad Request      │
│  │                          │
│  ├─ GitCommandError         │
│  │   → 500 Server Error     │
│  │                          │
│  ├─ FileNotFoundError       │
│  │   → 404 Not Found        │
│  │                          │
│  └─ Other                   │
│      → 500 Server Error     │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Return error response      │
│  {                          │
│    "result": "Error: ...",  │
│    "success": false         │
│  }                          │
└─────────────────────────────┘
```

## Monitoring Points

### Health Checks

```
Endpoint: GET /health

Response:
{
  "status": "healthy",
  "projects_configured": 1,
  "default_project": "thesis"
}

Checks:
✓ Server is running
✓ Configuration is loaded
✓ Projects are accessible
```

### Logging Points

```
1. Request received
   → Log: method, path, auth status

2. Tool execution start
   → Log: tool name, arguments

3. Git operations
   → Log: clone, pull, push, commit

4. Errors
   → Log: exception type, message, stack trace

5. Response sent
   → Log: status code, execution time
```

## Future Enhancements

### Planned Features

1. **Rate Limiting**
   ```python
   @limiter.limit("10/minute")
   async def edit_file(...):
   ```

2. **Webhooks**
   ```python
   @app.post("/webhooks/overleaf")
   async def overleaf_webhook(...):
       # Notify on external changes
   ```

3. **Caching**
   ```python
   @cache(expire=300)
   async def list_files(...):
   ```

4. **Metrics**
   ```python
   prometheus_client.Counter(
       'api_requests_total',
       'Total API requests'
   )
   ```

## Conclusion

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Multiple interface options (HTTP + MCP)
- ✅ Secure authentication
- ✅ Scalable design
- ✅ Easy deployment
- ✅ Comprehensive error handling

The system is production-ready and can handle typical thesis editing workloads with room for growth.

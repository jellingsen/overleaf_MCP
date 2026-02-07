# Quick Start Guide

Get your Overleaf MCP API running in 5 minutes.

## Local Testing (Before Deployment)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install
pip install -e .
```

### 2. Configure Overleaf

Create `overleaf_config.json`:

```json
{
  "projects": {
    "thesis": {
      "name": "My Thesis",
      "projectId": "YOUR_PROJECT_ID",
      "gitToken": "YOUR_GIT_TOKEN"
    }
  },
  "defaultProject": "thesis"
}
```

**Get your credentials:**
1. Open your Overleaf project
2. Project ID is in the URL: `https://www.overleaf.com/project/YOUR_PROJECT_ID`
3. Git token: Menu → Git → Generate token

### 3. Set API Key (Optional)

```bash
export API_KEY="your-secure-random-key"
```

Generate one with:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run the Server

```bash
# Easy way
./run_api.sh

# Or manually
uvicorn overleaf_mcp.fastapi_server:app --reload
```

Server runs at: http://localhost:8000

### 5. Test It

Open http://localhost:8000/docs for interactive API documentation.

Or use curl:

```bash
# Health check
curl http://localhost:8000/health

# List projects
curl http://localhost:8000/projects

# Read a file
curl -X POST http://localhost:8000/files/read \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"file_path": "main.tex"}}'

# With authentication
curl -X POST http://localhost:8000/files/read \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"file_path": "main.tex"}}'
```

## Deploy to DigitalOcean

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

**Quick version:**

1. Push code to GitHub
2. Create app on DigitalOcean App Platform
3. Connect your GitHub repo
4. Set environment variables:
   - `OVERLEAF_PROJECT_ID`
   - `OVERLEAF_GIT_TOKEN`
   - `API_KEY`
5. Deploy!

## Configure ChatGPT

1. Create a Custom GPT at https://chat.openai.com/
2. Add the OpenAPI schema from `openapi.yaml`
3. Set authentication: Bearer token with your `API_KEY`
4. Test with: "List all files in my thesis"

## Troubleshooting

**"No projects configured"**
- Check `overleaf_config.json` exists
- Or set `OVERLEAF_PROJECT_ID` and `OVERLEAF_GIT_TOKEN` env vars

**"Authentication failed"**
- Verify your Overleaf git token is correct
- Regenerate token in Overleaf if needed

**"Permission denied"**
- Ensure `overleaf_cache` directory is writable
- Check git is installed: `git --version`

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Check [README.md](README.md) for full API documentation
- See `openapi.yaml` for complete API specification

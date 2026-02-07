# Deployment Checklist

Use this checklist to deploy your Overleaf MCP API to DigitalOcean and connect it to ChatGPT.

## Prerequisites ✓

- [ ] Python 3.10+ installed
- [ ] Git installed
- [ ] Overleaf account with paid plan (for Git integration)
- [ ] GitHub account
- [ ] DigitalOcean account
- [ ] ChatGPT Plus subscription

## Phase 1: Local Setup (15 minutes)

### 1.1 Get Overleaf Credentials

- [ ] Open your Overleaf project in browser
- [ ] Copy Project ID from URL: `https://www.overleaf.com/project/YOUR_PROJECT_ID`
- [ ] Click Menu → Git → Generate token
- [ ] Copy the git token (between `git:` and `@` in the URL)

### 1.2 Configure Project

- [ ] Clone this repository
  ```bash
  git clone https://github.com/YOUR_USERNAME/overleaf-mcp.git
  cd overleaf-mcp
  ```

- [ ] Create virtual environment
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- [ ] Install dependencies
  ```bash
  pip install -e .
  ```

- [ ] Create configuration file
  ```bash
  cp overleaf_config.example.json overleaf_config.json
  ```

- [ ] Edit `overleaf_config.json` with your credentials
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

### 1.3 Test Locally

- [ ] Generate API key
  ```bash
  export API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  echo "Your API key: $API_KEY"
  ```

- [ ] Save your API key somewhere safe (you'll need it later)

- [ ] Start the server
  ```bash
  ./run_api.sh
  ```

- [ ] Open http://localhost:8000/docs in browser
- [ ] Verify API documentation loads

- [ ] Run tests
  ```bash
  python test_api.py
  ```

- [ ] Verify all tests pass ✓

## Phase 2: GitHub Setup (5 minutes)

### 2.1 Prepare Repository

- [ ] Verify `.gitignore` excludes secrets
  ```bash
  cat .gitignore | grep overleaf_config.json
  ```

- [ ] Commit all changes
  ```bash
  git add .
  git commit -m "Add FastAPI wrapper for ChatGPT"
  ```

### 2.2 Push to GitHub

- [ ] Create new repository on GitHub
  - Go to https://github.com/new
  - Name: `overleaf-mcp`
  - Visibility: Private (recommended)
  - Don't initialize with README

- [ ] Push code
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/overleaf-mcp.git
  git branch -M main
  git push -u origin main
  ```

- [ ] Verify code is on GitHub

## Phase 3: DigitalOcean Deployment (15 minutes)

### 3.1 Create App

- [ ] Log in to https://cloud.digitalocean.com/
- [ ] Click "Create" → "Apps"
- [ ] Choose "GitHub" as source
- [ ] Authorize DigitalOcean to access GitHub
- [ ] Select `overleaf-mcp` repository
- [ ] Choose `main` branch
- [ ] Enable "Autodeploy on push"

### 3.2 Configure App

- [ ] Set app name: `overleaf-thesis-api`
- [ ] Choose region (closest to you)
- [ ] Verify settings:
  - Type: Web Service
  - Dockerfile Path: `Dockerfile`
  - HTTP Port: `8000`

### 3.3 Set Environment Variables

Click "Edit" → "Environment Variables" and add:

- [ ] `OVERLEAF_PROJECT_ID`
  - Value: Your project ID
  - Type: Secret (encrypted)

- [ ] `OVERLEAF_GIT_TOKEN`
  - Value: Your git token
  - Type: Secret (encrypted)

- [ ] `API_KEY`
  - Value: Your generated API key
  - Type: Secret (encrypted)

Optional variables:

- [ ] `OVERLEAF_TEMP_DIR` = `/app/overleaf_cache`
- [ ] `OVERLEAF_CONFIG_FILE` = `/app/overleaf_config.json`

### 3.4 Choose Plan

- [ ] Select plan: Basic ($5/month)
- [ ] Instance size: Basic XXS (512 MB RAM)
- [ ] Review total cost: ~$5/month

### 3.5 Deploy

- [ ] Click "Create Resources"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Check build logs for errors
- [ ] Note your app URL: `https://overleaf-thesis-api-xxxxx.ondigitalocean.app`

### 3.6 Verify Deployment

- [ ] Test health endpoint
  ```bash
  curl https://your-app-url.ondigitalocean.app/health
  ```

- [ ] Verify response shows "healthy"

- [ ] Test with API key
  ```bash
  curl -X POST https://your-app-url.ondigitalocean.app/files/list \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"arguments": {}}'
  ```

- [ ] Run remote tests
  ```bash
  python test_api.py https://your-app-url.ondigitalocean.app YOUR_API_KEY
  ```

## Phase 4: ChatGPT Configuration (10 minutes)

### 4.1 Create Custom GPT

- [ ] Go to https://chat.openai.com/
- [ ] Click profile picture → "My GPTs"
- [ ] Click "Create a GPT"

### 4.2 Configure GPT

- [ ] Set name: "Overleaf Thesis Assistant"

- [ ] Set description:
  ```
  Helps manage and edit your Overleaf LaTeX thesis project
  ```

- [ ] Add instructions:
  ```
  You are an expert LaTeX thesis assistant. You help users:
  - Read and understand their thesis structure
  - Edit sections and chapters
  - Fix LaTeX errors and improve formatting
  - Add new content and files
  - Review commit history
  
  Always be precise with LaTeX syntax and preserve existing formatting.
  Ask for confirmation before major edits.
  ```

### 4.3 Add Actions

- [ ] Click "Create new action"

- [ ] Import OpenAPI schema:
  - Option A: Paste URL: `https://raw.githubusercontent.com/YOUR_USERNAME/overleaf-mcp/main/openapi.yaml`
  - Option B: Copy entire contents of `openapi.yaml` file

- [ ] Update server URL in schema:
  ```yaml
  servers:
    - url: https://your-app-url.ondigitalocean.app
  ```

- [ ] Verify schema is valid (no errors shown)

### 4.4 Configure Authentication

- [ ] In Actions panel, click "Authentication"
- [ ] Choose "API Key"
- [ ] Set Auth Type: "Bearer"
- [ ] Enter API Key: Your `API_KEY` from DigitalOcean
- [ ] Save

### 4.5 Test GPT

- [ ] Click "Test" in GPT builder

- [ ] Try: "List all files in my thesis"
  - [ ] Verify it returns your files

- [ ] Try: "Read main.tex"
  - [ ] Verify it shows file content

- [ ] Try: "What sections are in chapter1.tex?"
  - [ ] Verify it parses sections

- [ ] Try: "Show me the last 5 commits"
  - [ ] Verify it shows git history

### 4.6 Publish GPT

- [ ] Click "Save" in top right
- [ ] Choose visibility:
  - "Only me" (recommended for thesis work)
  - "Anyone with a link" (if sharing)
  - "Public" (not recommended for personal thesis)

- [ ] Click "Confirm"

## Phase 5: Final Verification (5 minutes)

### 5.1 End-to-End Test

- [ ] Open your Custom GPT in ChatGPT

- [ ] Test read operation:
  ```
  "List all .tex files in my thesis"
  ```
  - [ ] Verify files are listed

- [ ] Test section parsing:
  ```
  "What sections are in main.tex?"
  ```
  - [ ] Verify sections are parsed

- [ ] Test edit operation (be careful!):
  ```
  "In main.tex, replace 'TODO' with 'DONE' if it exists"
  ```
  - [ ] Verify edit is made
  - [ ] Check Overleaf web editor shows change

- [ ] Test git history:
  ```
  "Show me the last commit"
  ```
  - [ ] Verify your edit appears in history

### 5.2 Verify Overleaf Sync

- [ ] Open your Overleaf project in browser
- [ ] Check that changes from ChatGPT appear
- [ ] Verify git history shows commits from "Overleaf MCP"

## Phase 6: Documentation (5 minutes)

### 6.1 Save Important Information

Create a file `DEPLOYMENT_INFO.txt` with:

```
DigitalOcean App URL: https://your-app-url.ondigitalocean.app
API Key: YOUR_API_KEY
Overleaf Project ID: YOUR_PROJECT_ID
ChatGPT GPT Link: https://chat.openai.com/g/g-YOUR_GPT_ID
Deployment Date: YYYY-MM-DD
```

- [ ] Save this file securely (NOT in git!)

### 6.2 Update Documentation

- [ ] Update `README.md` with your specific URLs
- [ ] Update `openapi.yaml` with your app URL
- [ ] Commit and push changes

## Troubleshooting Checklist

If something doesn't work, check:

### API Issues

- [ ] DigitalOcean app is running (check dashboard)
- [ ] Environment variables are set correctly
- [ ] API key matches in DigitalOcean and ChatGPT
- [ ] Health endpoint returns 200 OK
- [ ] Check runtime logs in DigitalOcean

### ChatGPT Issues

- [ ] OpenAPI schema is valid
- [ ] Server URL is correct in schema
- [ ] Authentication is configured
- [ ] API key is correct
- [ ] Try regenerating the action

### Overleaf Issues

- [ ] Git token is valid (not expired)
- [ ] Project ID is correct
- [ ] Git integration is enabled (paid plan)
- [ ] Try regenerating git token in Overleaf

### Git Issues

- [ ] Git is installed in Docker container
- [ ] Cache directory is writable
- [ ] No merge conflicts
- [ ] Network connectivity to git.overleaf.com

## Success Criteria

You're done when:

- [x] Local server runs without errors
- [x] Tests pass locally
- [x] Code is on GitHub
- [x] App is deployed on DigitalOcean
- [x] Health check returns "healthy"
- [x] ChatGPT Custom GPT is created
- [x] ChatGPT can list your files
- [x] ChatGPT can read file content
- [x] ChatGPT can edit files
- [x] Changes appear in Overleaf
- [x] Git history shows commits

## Next Steps

After successful deployment:

- [ ] Set up monitoring alerts in DigitalOcean
- [ ] Configure custom domain (optional)
- [ ] Add rate limiting (optional)
- [ ] Set up automated backups
- [ ] Create additional specialized GPTs
- [ ] Share with collaborators (optional)

## Maintenance Schedule

### Weekly
- [ ] Check DigitalOcean app status
- [ ] Review runtime logs for errors
- [ ] Verify git sync is working

### Monthly
- [ ] Review API usage and costs
- [ ] Update dependencies if needed
- [ ] Rotate API key (optional)
- [ ] Check for Overleaf updates

### As Needed
- [ ] Scale up if performance issues
- [ ] Update GPT instructions
- [ ] Add new features
- [ ] Fix bugs

## Cost Tracking

| Service | Plan | Monthly Cost |
|---------|------|--------------|
| DigitalOcean App Platform | Basic XXS | $5 |
| ChatGPT Plus | Plus | $20 |
| **Total** | | **$25** |

## Support Resources

- [ ] Bookmark these docs:
  - DigitalOcean: https://docs.digitalocean.com/products/app-platform/
  - OpenAI GPTs: https://help.openai.com/en/articles/8554397
  - Overleaf Git: https://www.overleaf.com/learn/how-to/Using_Git_and_GitHub

- [ ] Join communities:
  - DigitalOcean Community: https://www.digitalocean.com/community
  - OpenAI Forum: https://community.openai.com/

## Completion

- [ ] All phases completed
- [ ] System is working end-to-end
- [ ] Documentation is saved
- [ ] Backup of configuration exists

**Congratulations! Your Overleaf thesis is now accessible to ChatGPT! 🎓**

---

**Estimated Total Time: 55 minutes**

**Total Cost: ~$25/month**

**Difficulty: Intermediate**

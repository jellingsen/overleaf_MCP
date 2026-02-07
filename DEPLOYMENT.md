# Deploying Overleaf MCP API to DigitalOcean App Platform

This guide walks you through deploying the FastAPI-wrapped Overleaf MCP server to DigitalOcean App Platform, making it accessible to ChatGPT.

## Prerequisites

1. **DigitalOcean Account**: Sign up at https://www.digitalocean.com/
2. **GitHub Account**: Your code needs to be in a GitHub repository
3. **Overleaf Credentials**: Project ID and Git Token from your Overleaf project

## Step 1: Prepare Your Repository

### 1.1 Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit with FastAPI wrapper"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/overleaf-mcp.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Files

Ensure these files are in your repository:
- `Dockerfile`
- `requirements.txt`
- `src/overleaf_mcp/fastapi_server.py`
- `.do/app.yaml` (optional, for automated deployment)

## Step 2: Deploy to DigitalOcean

### Option A: Using the Web Console (Recommended for First Time)

1. **Log in to DigitalOcean**
   - Go to https://cloud.digitalocean.com/

2. **Create New App**
   - Click "Create" → "Apps"
   - Choose "GitHub" as the source
   - Authorize DigitalOcean to access your GitHub account
   - Select your `overleaf-mcp` repository
   - Choose the `main` branch
   - Enable "Autodeploy" (deploys on every push)

3. **Configure the App**
   - **Name**: `overleaf-mcp-api`
   - **Region**: Choose closest to you (e.g., New York, San Francisco, London)
   - **Type**: Web Service
   - **Dockerfile Path**: `Dockerfile`
   - **HTTP Port**: `8000`

4. **Set Environment Variables**
   
   Click "Edit" next to your service, then go to "Environment Variables":
   
   **Required Variables:**
   ```
   OVERLEAF_PROJECT_ID = your_overleaf_project_id
   OVERLEAF_GIT_TOKEN = your_overleaf_git_token
   API_KEY = generate_a_secure_random_key_here
   ```
   
   **Optional Variables:**
   ```
   OVERLEAF_TEMP_DIR = /app/overleaf_cache
   OVERLEAF_CONFIG_FILE = /app/overleaf_config.json
   ```
   
   **Generate a secure API key:**
   ```bash
   # On macOS/Linux:
   openssl rand -hex 32
   
   # Or use Python:
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Choose Plan**
   - Start with **Basic** plan ($5/month)
   - Instance size: **Basic XXS** (512 MB RAM, 1 vCPU) is sufficient for light use
   - Scale up if needed later

6. **Review and Create**
   - Review all settings
   - Click "Create Resources"
   - Wait 5-10 minutes for deployment

7. **Get Your API URL**
   - Once deployed, you'll see a URL like: `https://overleaf-mcp-api-xxxxx.ondigitalocean.app`
   - Test it: `curl https://your-app-url.ondigitalocean.app/health`

### Option B: Using doctl CLI

```bash
# Install doctl
brew install doctl  # macOS
# Or download from: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Authenticate
doctl auth init

# Create app from spec
doctl apps create --spec .do/app.yaml

# Set secrets (after app is created)
doctl apps update YOUR_APP_ID --env API_KEY=your_secure_key
doctl apps update YOUR_APP_ID --env OVERLEAF_PROJECT_ID=your_project_id
doctl apps update YOUR_APP_ID --env OVERLEAF_GIT_TOKEN=your_git_token
```

## Step 3: Test Your Deployment

### 3.1 Health Check

```bash
curl https://your-app-url.ondigitalocean.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "projects_configured": 1,
  "default_project": "default"
}
```

### 3.2 List Projects (No Auth Required)

```bash
curl https://your-app-url.ondigitalocean.app/projects
```

### 3.3 Read a File (With Auth)

```bash
curl -X POST https://your-app-url.ondigitalocean.app/files/read \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"file_path": "main.tex"}}'
```

## Step 4: Configure ChatGPT Custom GPT

### 4.1 Create a Custom GPT

1. Go to https://chat.openai.com/
2. Click your profile → "My GPTs" → "Create a GPT"
3. Name it: "Overleaf Thesis Assistant"

### 4.2 Add Instructions

```
You are an assistant that helps manage Overleaf LaTeX projects. You can:
- Read and list files in the thesis project
- View and edit sections of LaTeX documents
- Create new files and update existing ones
- View commit history and changes

Always be helpful and precise when editing LaTeX content.
```

### 4.3 Configure Actions

Click "Create new action" and add this OpenAPI schema:

```yaml
openapi: 3.1.0
info:
  title: Overleaf MCP API
  version: 1.0.0
servers:
  - url: https://your-app-url.ondigitalocean.app

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer

security:
  - BearerAuth: []

paths:
  /projects:
    get:
      operationId: listProjects
      summary: List all configured Overleaf projects
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: string
                  success:
                    type: boolean

  /files/list:
    post:
      operationId: listFiles
      summary: List files in a project
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  properties:
                    extension:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /files/read:
    post:
      operationId: readFile
      summary: Read a file's content
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                  properties:
                    file_path:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /sections/list:
    post:
      operationId: getSections
      summary: Get sections from a LaTeX file
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                  properties:
                    file_path:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /sections/read:
    post:
      operationId: getSectionContent
      summary: Get content of a specific section
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                    - section_title
                  properties:
                    file_path:
                      type: string
                    section_title:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /files/edit:
    post:
      operationId: editFile
      summary: Edit a file with surgical replacement
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                    - old_string
                    - new_string
                  properties:
                    file_path:
                      type: string
                    old_string:
                      type: string
                    new_string:
                      type: string
                    commit_message:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /sections/update:
    post:
      operationId: updateSection
      summary: Update a specific section
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                    - section_title
                    - new_content
                  properties:
                    file_path:
                      type: string
                    section_title:
                      type: string
                    new_content:
                      type: string
                    commit_message:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success

  /files/create:
    post:
      operationId: createFile
      summary: Create a new file
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                arguments:
                  type: object
                  required:
                    - file_path
                    - content
                  properties:
                    file_path:
                      type: string
                    content:
                      type: string
                    commit_message:
                      type: string
                    project_name:
                      type: string
      responses:
        '200':
          description: Success
```

### 4.4 Add Authentication

In the Actions configuration:
- **Authentication Type**: API Key
- **Auth Type**: Bearer
- **API Key**: Your `API_KEY` from environment variables

### 4.5 Test in ChatGPT

Try these prompts:
- "List all files in my thesis"
- "Read the content of main.tex"
- "What sections are in chapter1.tex?"
- "Update the Introduction section with this new text: ..."

## Step 5: Monitoring and Maintenance

### View Logs

```bash
# Using doctl
doctl apps logs YOUR_APP_ID --type run

# Or in the web console:
# Apps → Your App → Runtime Logs
```

### Update Deployment

```bash
# Push changes to GitHub
git add .
git commit -m "Update API"
git push

# DigitalOcean will auto-deploy if you enabled it
```

### Scale Up/Down

In the DigitalOcean console:
- Go to your app → Settings → Components
- Change instance size or count
- Click "Save" to apply

## Troubleshooting

### "Authentication failed" errors
- Verify `OVERLEAF_GIT_TOKEN` is correct
- Check if token has expired in Overleaf settings

### "No projects configured"
- Ensure `OVERLEAF_PROJECT_ID` and `OVERLEAF_GIT_TOKEN` are set
- Check environment variables in DigitalOcean console

### API returns 401 Unauthorized
- Verify `API_KEY` matches in both DigitalOcean and ChatGPT
- Check Authorization header format: `Bearer YOUR_KEY`

### App won't start
- Check runtime logs in DigitalOcean console
- Verify Dockerfile builds locally: `docker build -t test .`
- Ensure all dependencies are in `requirements.txt`

### Git operations fail
- Check if `/app/overleaf_cache` directory is writable
- Verify git is installed in Docker image

## Cost Estimation

**DigitalOcean App Platform Pricing:**
- Basic XXS: $5/month (512 MB RAM, 1 vCPU)
- Basic XS: $12/month (1 GB RAM, 1 vCPU)
- Professional: Starting at $12/month with more resources

**Recommended for personal thesis:**
- Start with Basic XXS ($5/month)
- Upgrade if you experience slowness

## Security Best Practices

1. **Rotate API Keys**: Change your `API_KEY` periodically
2. **Use Secrets**: Store sensitive values as encrypted secrets in DigitalOcean
3. **Enable HTTPS**: DigitalOcean provides free SSL certificates
4. **Limit CORS**: The API only allows requests from ChatGPT domains
5. **Monitor Logs**: Check for suspicious activity regularly

## Next Steps

- Set up monitoring alerts in DigitalOcean
- Configure custom domain (optional)
- Add rate limiting for production use
- Set up automated backups of your Overleaf cache

## Support

- DigitalOcean Docs: https://docs.digitalocean.com/products/app-platform/
- Overleaf Git: https://www.overleaf.com/learn/how-to/Using_Git_and_GitHub
- FastAPI Docs: https://fastapi.tiangolo.com/

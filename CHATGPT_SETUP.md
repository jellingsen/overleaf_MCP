# ChatGPT Custom GPT Setup Guide

Complete guide to connecting your Overleaf thesis to ChatGPT.

## Overview

This setup allows you to:
- Ask ChatGPT to read your thesis files
- Edit sections directly from ChatGPT
- Create new files and chapters
- View commit history and changes
- All changes sync automatically to Overleaf

## Architecture

```
┌─────────────┐         HTTPS          ┌──────────────────┐
│   ChatGPT   │◄──────────────────────►│  DigitalOcean    │
│  (Browser)  │    OpenAPI Actions     │   FastAPI App    │
└─────────────┘                        └────────┬─────────┘
                                                │
                                                │ Git HTTPS
                                                ▼
                                       ┌──────────────────┐
                                       │     Overleaf     │
                                       │   Git Server     │
                                       └──────────────────┘
```

## Step-by-Step Setup

### Phase 1: Deploy to DigitalOcean (15 minutes)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add FastAPI wrapper"
   git push origin main
   ```

2. **Create DigitalOcean App**
   - Go to https://cloud.digitalocean.com/
   - Click "Create" → "Apps"
   - Connect your GitHub repository
   - Select the `overleaf-mcp` repo
   - Choose `main` branch

3. **Configure the app**
   - Name: `overleaf-thesis-api`
   - Region: Choose closest to you
   - Dockerfile: `Dockerfile`
   - HTTP Port: `8000`

4. **Set environment variables**
   
   In DigitalOcean App settings, add these as encrypted secrets:
   
   ```
   OVERLEAF_PROJECT_ID = <your_project_id>
   OVERLEAF_GIT_TOKEN = <your_git_token>
   API_KEY = <generate_secure_random_key>
   ```
   
   Generate API key:
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Deploy**
   - Click "Create Resources"
   - Wait 5-10 minutes
   - Note your app URL: `https://overleaf-thesis-api-xxxxx.ondigitalocean.app`

6. **Test deployment**
   ```bash
   curl https://your-app-url.ondigitalocean.app/health
   ```

### Phase 2: Create Custom GPT (10 minutes)

1. **Go to ChatGPT**
   - Visit https://chat.openai.com/
   - Click your profile picture
   - Select "My GPTs"
   - Click "Create a GPT"

2. **Configure GPT**
   
   **Name:**
   ```
   Overleaf Thesis Assistant
   ```
   
   **Description:**
   ```
   Helps manage and edit your Overleaf LaTeX thesis project
   ```
   
   **Instructions:**
   ```
   You are an expert LaTeX thesis assistant. You help users:
   - Read and understand their thesis structure
   - Edit sections and chapters
   - Fix LaTeX errors and improve formatting
   - Add new content and files
   - Review commit history
   
   Always:
   - Be precise with LaTeX syntax
   - Preserve existing formatting and structure
   - Explain changes you make
   - Ask for confirmation before major edits
   
   When editing:
   - Use edit_file for small changes
   - Use update_section for section-level changes
   - Use rewrite_file only when necessary
   ```

3. **Add Actions**
   
   Click "Create new action" and paste the OpenAPI schema from `openapi.yaml`.
   
   **Quick version - paste this URL in the schema import:**
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/overleaf-mcp/main/openapi.yaml
   ```
   
   Or copy the entire contents of `openapi.yaml` into the schema editor.

4. **Configure Authentication**
   
   In the Actions panel:
   - Authentication Type: **API Key**
   - Auth Type: **Bearer**
   - API Key: `<your_API_KEY_from_digitalocean>`

5. **Test the GPT**
   
   Try these prompts:
   ```
   "List all files in my thesis"
   "Read the introduction section"
   "What chapters do I have?"
   "Show me the last 5 commits"
   ```

### Phase 3: Using Your GPT

#### Reading Content

```
"List all .tex files"
"Read main.tex"
"What sections are in chapter1.tex?"
"Show me the abstract"
"Get the content of the Methods section"
```

#### Editing Content

```
"Fix the typo in the introduction where it says 'teh' instead of 'the'"
"Update the Abstract section with this new text: [paste text]"
"Add a new subsection called 'Future Work' to chapter 5"
"Rewrite the conclusion to be more concise"
```

#### Creating Files

```
"Create a new file called appendix.tex with a section for supplementary materials"
"Add a new chapter file chapter6.tex about conclusions"
"Create a bibliography file references.bib"
```

#### Project Management

```
"Show me the last 10 commits"
"What changed in the last week?"
"Sync the project to get latest changes"
"Show me the diff for main.tex"
```

## Security Best Practices

1. **API Key Protection**
   - Never share your API key
   - Rotate it periodically
   - Store it as an encrypted secret in DigitalOcean

2. **Access Control**
   - Only you can access your Custom GPT (unless you publish it)
   - API is protected by Bearer token authentication
   - CORS is restricted to ChatGPT domains

3. **Git Token Security**
   - Git token provides full read/write access to your Overleaf project
   - Store as encrypted secret in DigitalOcean
   - Regenerate if compromised

## Troubleshooting

### "Action failed" in ChatGPT

**Check API is running:**
```bash
curl https://your-app-url.ondigitalocean.app/health
```

**Check logs in DigitalOcean:**
- Go to your app → Runtime Logs
- Look for errors

### "Authentication failed"

**Verify API key:**
- Check it matches in both DigitalOcean and ChatGPT
- Ensure format is: `Bearer YOUR_KEY` (ChatGPT adds "Bearer" automatically)

### "No projects configured"

**Check environment variables:**
- Go to DigitalOcean app → Settings → Environment Variables
- Verify `OVERLEAF_PROJECT_ID` and `OVERLEAF_GIT_TOKEN` are set
- Redeploy if you changed them

### "File not found"

**Sync project first:**
```
"Sync the project"
```

Then try again.

### GPT doesn't see the actions

**Verify OpenAPI schema:**
- Go to GPT configuration → Actions
- Check schema is valid (no errors shown)
- Ensure authentication is configured

## Cost Breakdown

**DigitalOcean:**
- Basic XXS: $5/month (sufficient for personal use)
- Basic XS: $12/month (if you need more resources)

**ChatGPT:**
- Requires ChatGPT Plus ($20/month)
- Custom GPTs are included in Plus subscription

**Total: $25-32/month**

## Advanced Configuration

### Multiple Projects

Edit environment variables in DigitalOcean to use JSON config:

```json
{
  "projects": {
    "thesis": {
      "name": "PhD Thesis",
      "projectId": "project_id_1",
      "gitToken": "token_1"
    },
    "paper": {
      "name": "Research Paper",
      "projectId": "project_id_2",
      "gitToken": "token_2"
    }
  },
  "defaultProject": "thesis"
}
```

Save as `overleaf_config.json` and mount in DigitalOcean.

### Custom Domain

In DigitalOcean:
- Go to Settings → Domains
- Add your custom domain
- Update DNS records
- Update OpenAPI schema in ChatGPT with new domain

### Rate Limiting

Add to `fastapi_server.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/files/edit")
@limiter.limit("10/minute")
async def edit_file(request: Request, ...):
    ...
```

## Tips for Best Results

1. **Be specific**: "Edit chapter1.tex and fix the typo in line 45" works better than "fix typos"

2. **Use section names**: "Update the Introduction section" is more reliable than "edit the first section"

3. **Review changes**: Always ask to see the diff before major edits

4. **Commit messages**: The GPT will generate commit messages, but you can specify them: "Update the abstract (commit message: 'Revise abstract for clarity')"

5. **Sync regularly**: Start conversations with "Sync the project" to ensure you have the latest version

## Next Steps

- Set up monitoring alerts in DigitalOcean
- Configure automatic backups
- Add more custom instructions to your GPT
- Create additional GPTs for specific tasks (e.g., "Bibliography Manager", "LaTeX Formatter")

## Support Resources

- **DigitalOcean Docs**: https://docs.digitalocean.com/products/app-platform/
- **OpenAI Custom GPTs**: https://help.openai.com/en/articles/8554397-creating-a-gpt
- **Overleaf Git**: https://www.overleaf.com/learn/how-to/Using_Git_and_GitHub
- **FastAPI Docs**: https://fastapi.tiangolo.com/

## Example Conversation

```
You: "List all files in my thesis"

GPT: "I found these files in your thesis:
- main.tex
- chapter1.tex
- chapter2.tex
- chapter3.tex
- references.bib
- abstract.tex

Would you like me to read any of these files?"

You: "Read the abstract"

GPT: [Shows abstract content]

You: "Update it to be more concise, focusing on the key findings"

GPT: "I'll update the abstract section. Here's what I'll change:
[Shows proposed changes]

Should I proceed with this update?"

You: "Yes, go ahead"

GPT: "Done! I've updated the abstract and pushed the changes to Overleaf. 
The commit message is: 'Revise abstract for conciseness and clarity'"
```

---

**You're all set!** Your thesis is now accessible to ChatGPT. Happy writing! 🎓

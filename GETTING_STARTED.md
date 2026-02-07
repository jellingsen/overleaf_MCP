# Getting Started with Overleaf MCP API

Welcome! This guide will help you get your Overleaf thesis connected to ChatGPT in under an hour.

## What You're Building

A system that lets you use ChatGPT to:
- Read your thesis files
- Edit sections and chapters
- Create new files
- View commit history
- All synced automatically with Overleaf

## Choose Your Path

### 🚀 Quick Start (Just want to try it?)
**Time: 5 minutes**

1. Install and run locally:
   ```bash
   pip install -e .
   cp overleaf_config.example.json overleaf_config.json
   # Edit overleaf_config.json with your credentials
   ./run_api.sh
   ```

2. Visit http://localhost:8000/docs

3. See [QUICKSTART.md](QUICKSTART.md) for details

### 📋 Full Deployment (Ready to use with ChatGPT?)
**Time: 55 minutes**

Follow the complete checklist:
1. [CHECKLIST.md](CHECKLIST.md) - Step-by-step deployment guide

Or read the detailed guides:
1. [DEPLOYMENT.md](DEPLOYMENT.md) - DigitalOcean deployment
2. [CHATGPT_SETUP.md](CHATGPT_SETUP.md) - ChatGPT configuration

### 📚 Want to Understand How It Works?
**Time: 15 minutes**

Read the architecture documentation:
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design and data flow
2. [SUMMARY.md](SUMMARY.md) - Project overview

## Prerequisites

Before you start, you need:

- ✅ Python 3.10+ installed
- ✅ Git installed
- ✅ Overleaf account with paid plan (for Git integration)
- ✅ GitHub account (for deployment)
- ✅ DigitalOcean account (for hosting)
- ✅ ChatGPT Plus subscription (for Custom GPTs)

**Don't have these?** You can still test locally without DigitalOcean or ChatGPT Plus.

## Quick Reference

### Get Overleaf Credentials

1. **Project ID**: From URL `https://www.overleaf.com/project/YOUR_PROJECT_ID`
2. **Git Token**: Menu → Git → Generate token

### Generate API Key

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Test Locally

```bash
./run_api.sh
# Visit http://localhost:8000/docs
```

### Test API

```bash
python test_api.py
```

### Deploy to DigitalOcean

1. Push to GitHub
2. Create app on DigitalOcean
3. Set environment variables
4. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

### Configure ChatGPT

1. Create Custom GPT
2. Import `openapi.yaml`
3. Set Bearer token authentication
4. Test with "List all files"

See [CHATGPT_SETUP.md](CHATGPT_SETUP.md) for details.

## Documentation Index

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** ← You are here
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute local setup
- **[CHECKLIST.md](CHECKLIST.md)** - Complete deployment checklist

### Deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - DigitalOcean deployment guide
- **[CHATGPT_SETUP.md](CHATGPT_SETUP.md)** - ChatGPT Custom GPT setup

### Technical
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[SUMMARY.md](SUMMARY.md)** - Project overview
- **[README.md](README.md)** - Main documentation

### Reference
- **[openapi.yaml](openapi.yaml)** - API specification
- **[Dockerfile](Dockerfile)** - Container configuration
- **[.do/app.yaml](.do/app.yaml)** - DigitalOcean app spec

## Common Questions

### Do I need to pay for anything?

**For local testing:** No, it's free.

**For ChatGPT integration:**
- DigitalOcean: $5/month (Basic XXS plan)
- ChatGPT Plus: $20/month
- Total: $25/month

### Can I use this without ChatGPT?

Yes! The API works with:
- Claude Desktop (original MCP protocol)
- Any HTTP client (curl, Postman, etc.)
- Your own applications

### Is my thesis data secure?

Yes:
- API requires authentication (Bearer token)
- All traffic is HTTPS encrypted
- Secrets stored encrypted in DigitalOcean
- CORS restricted to ChatGPT domains
- Your thesis stays on Overleaf

### What if I have multiple projects?

Configure multiple projects in `overleaf_config.json`:

```json
{
  "projects": {
    "thesis": { ... },
    "paper": { ... }
  },
  "defaultProject": "thesis"
}
```

### Can I self-host instead of DigitalOcean?

Yes! The Docker container runs anywhere:
- AWS, Google Cloud, Azure
- Your own server
- Kubernetes cluster
- Any Docker host

### What if something breaks?

1. Check [CHECKLIST.md](CHECKLIST.md) troubleshooting section
2. Review logs in DigitalOcean
3. Test locally with `./run_api.sh`
4. Run `python test_api.py` to diagnose

## Example Usage

Once deployed, you can ask ChatGPT:

```
"List all files in my thesis"
"Read the introduction section"
"Fix the typo in chapter 1 where it says 'teh' instead of 'the'"
"Add a new section called 'Future Work' to the conclusion"
"Show me the last 10 commits"
"What changed in the last week?"
```

## Next Steps

1. **Start here**: [QUICKSTART.md](QUICKSTART.md) for local testing
2. **Then deploy**: [CHECKLIST.md](CHECKLIST.md) for full deployment
3. **Learn more**: [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

## Need Help?

- Check the troubleshooting sections in each guide
- Review the test scripts: `python test_api.py`
- Read the architecture docs: [ARCHITECTURE.md](ARCHITECTURE.md)
- Check DigitalOcean logs for errors

## Success Stories

After setup, you'll be able to:
- ✅ Edit your thesis from ChatGPT
- ✅ Get AI help with LaTeX formatting
- ✅ Review and improve sections
- ✅ Track all changes in git history
- ✅ Sync automatically with Overleaf

## Time Investment

- **Local testing**: 5 minutes
- **Full deployment**: 55 minutes
- **Learning architecture**: 15 minutes
- **Total**: ~1 hour for complete setup

## Cost Summary

| Component | Cost | Required For |
|-----------|------|--------------|
| Local testing | Free | Testing |
| DigitalOcean | $5/mo | ChatGPT integration |
| ChatGPT Plus | $20/mo | Custom GPTs |
| **Total** | **$25/mo** | Full setup |

## Ready to Start?

Pick your path:

- 🏃 **Quick test**: [QUICKSTART.md](QUICKSTART.md)
- 📋 **Full setup**: [CHECKLIST.md](CHECKLIST.md)
- 📖 **Learn first**: [ARCHITECTURE.md](ARCHITECTURE.md)

**Let's get your thesis connected to ChatGPT! 🎓**

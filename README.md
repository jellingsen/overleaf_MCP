# Overleaf MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides full CRUD operations for [Overleaf](https://www.overleaf.com/) LaTeX projects. Enables AI assistants to read, edit, create, and delete files in your Overleaf projects.

**Now with FastAPI wrapper for ChatGPT integration!** Deploy to DigitalOcean and access your thesis from ChatGPT web interface.

## 🚀 Quick Start

**New here?** Start with [GETTING_STARTED.md](GETTING_STARTED.md) for a guided introduction.

**Want to deploy?** Follow [CHECKLIST.md](CHECKLIST.md) for step-by-step instructions.

**Just testing?** Run `./run_api.sh` and visit http://localhost:8000/docs

## How It Works

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   ChatGPT   │◄───────►│  FastAPI on  │◄───────►│  Overleaf   │
│  (Browser)  │  HTTPS  │ DigitalOcean │   Git   │   Server    │
└─────────────┘         └──────────────┘         └─────────────┘
```

1. Ask ChatGPT to edit your thesis
2. API processes request and updates files
3. Changes sync automatically to Overleaf
4. View updates in Overleaf web editor

## Features

### 14 Tools for Complete Project Management

| Category | Tool | Description |
|----------|------|-------------|
| **Create** | `create_project` | Create new Overleaf projects from LaTeX content or ZIP files |
| | `create_file` | Add new files to existing projects |
| **Read** | `list_projects` | View all configured projects |
| | `list_files` | List files with optional extension filter |
| | `read_file` | Read file contents |
| | `get_sections` | Parse LaTeX structure (chapters, sections, subsections) |
| | `get_section_content` | Get full content of a specific section |
| | `list_history` | View git commit history |
| | `get_diff` | Compare changes between versions |
| **Update** | `edit_file` | **Surgical edit** - replace specific text (old_string → new_string) |
| | `rewrite_file` | Replace entire file contents |
| | `update_section` | Update a specific LaTeX section by title |
| | `sync_project` | Pull latest changes from Overleaf |
| **Delete** | `delete_file` | Remove files from projects |

### Key Capabilities

- **Git Integration**: Uses Overleaf's Git integration for reliable sync
- **Multi-Project Support**: Configure and switch between multiple projects
- **LaTeX-Aware**: Understands document structure for section-based operations
- **Auto-Push**: All write operations commit and push to Overleaf immediately
- **Local Caching**: Fast access with local repository cache

---

## Installation

### Prerequisites

- Python 3.10+
- Git
- Overleaf account with Git integration (requires paid plan)

### For MCP Usage (Claude Desktop, etc.)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/overleaf-mcp.git
cd overleaf-mcp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install
pip install -e .
```

### For ChatGPT / HTTP API Usage

See [QUICKSTART.md](QUICKSTART.md) for local testing, or [DEPLOYMENT.md](DEPLOYMENT.md) for deploying to DigitalOcean.

**Quick start:**
```bash
pip install -e .
./run_api.sh
# API runs at http://localhost:8000
```

---

## Configuration

### Step 1: Get Your Overleaf Credentials

1. **Open your Overleaf project** in the browser

2. **Get Project ID** from the URL:
   ```
   https://www.overleaf.com/project/YOUR_PROJECT_ID
                                    ^^^^^^^^^^^^^^^^
   ```

3. **Get Git Token**:
   - Click **Menu** (top-left)
   - Click **Git** under "Sync"
   - Click **Generate token** (if not already generated)
   - Copy the URL: `https://git:YOUR_TOKEN@git.overleaf.com/...`
   - Extract the token (the part between `git:` and `@`)

### Step 2: Create Configuration File

Create `overleaf_config.json` in the project directory:

```json
{
  "projects": {
    "my-thesis": {
      "name": "My PhD Thesis",
      "projectId": "abc123def456",
      "gitToken": "olp_xxxxxxxxxxxxxxxxxxxx"
    },
    "paper": {
      "name": "Research Paper",
      "projectId": "xyz789ghi012",
      "gitToken": "olp_yyyyyyyyyyyyyyyyyyyy"
    }
  },
  "defaultProject": "my-thesis"
}
```

### Alternative: Environment Variables

For single-project setups:

```bash
export OVERLEAF_PROJECT_ID="your_project_id"
export OVERLEAF_GIT_TOKEN="your_git_token"
```

---

## Client Configuration

### ChatGPT (Web Browser)

Deploy the FastAPI wrapper to DigitalOcean and configure a Custom GPT:

1. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to DigitalOcean App Platform
2. **Create Custom GPT**: Go to https://chat.openai.com/ → My GPTs → Create
3. **Add Actions**: Import the OpenAPI schema from `openapi.yaml`
4. **Authenticate**: Use Bearer token with your API key

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

### Claude Desktop

**Config file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "overleaf": {
      "command": "/path/to/overleaf-mcp/.venv/bin/python",
      "args": ["-m", "overleaf_mcp.server"],
      "cwd": "/path/to/overleaf-mcp",
      "env": {
        "OVERLEAF_CONFIG_FILE": "/path/to/overleaf-mcp/overleaf_config.json",
        "OVERLEAF_TEMP_DIR": "/path/to/overleaf-mcp/overleaf_cache"
      }
    }
  }
}
```

**Example (macOS):**

```json
{
  "mcpServers": {
    "overleaf": {
      "command": "/Users/username/dev/overleaf-mcp/.venv/bin/python",
      "args": ["-m", "overleaf_mcp.server"],
      "cwd": "/Users/username/dev/overleaf-mcp",
      "env": {
        "OVERLEAF_CONFIG_FILE": "/Users/username/dev/overleaf-mcp/overleaf_config.json",
        "OVERLEAF_TEMP_DIR": "/Users/username/dev/overleaf-mcp/overleaf_cache"
      }
    }
  }
}
```

After saving, **restart Claude Desktop** (Cmd+Q / Ctrl+Q, then reopen).

---

### Claude Code (CLI)

Add to your Claude Code MCP settings (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "overleaf": {
      "command": "/path/to/overleaf-mcp/.venv/bin/python",
      "args": ["-m", "overleaf_mcp.server"],
      "cwd": "/path/to/overleaf-mcp",
      "env": {
        "OVERLEAF_CONFIG_FILE": "/path/to/overleaf-mcp/overleaf_config.json",
        "OVERLEAF_TEMP_DIR": "/path/to/overleaf-mcp/overleaf_cache"
      }
    }
  }
}
```

Or add per-project in `.claude/settings.json` in your project directory.

---

### VS Code (with Claude Extension)

Add to your VS Code settings (`settings.json`):

```json
{
  "claude.mcpServers": {
    "overleaf": {
      "command": "/path/to/overleaf-mcp/.venv/bin/python",
      "args": ["-m", "overleaf_mcp.server"],
      "cwd": "/path/to/overleaf-mcp",
      "env": {
        "OVERLEAF_CONFIG_FILE": "/path/to/overleaf-mcp/overleaf_config.json",
        "OVERLEAF_TEMP_DIR": "/path/to/overleaf-mcp/overleaf_cache"
      }
    }
  }
}
```

**Or** add to workspace settings (`.vscode/settings.json`) for project-specific config.

---

## Usage Examples

Once configured, you can ask the AI assistant:

### Reading Files
```
"List all .tex files in my thesis"
"Read the content of main.tex"
"What sections are in chapter1.tex?"
```

### Editing Content
```
"Edit main.tex and replace 'teh' with 'the'"
"Rewrite the abstract.tex file with this new content: ..."
"Update the 'Introduction' section with this new content: ..."
```

### Creating Files
```
"Create a new file called appendix.tex with a section for supplementary materials"
"Add a new bibliography file references.bib"
```

### Project Management
```
"Show me the last 10 commits"
"What changed since yesterday?"
"Sync the project to get latest changes"
```

### Section-Based Operations
```
"Get the content of the 'Methods' section"
"Update the 'Results' section with these findings: ..."
"What subsections are in chapter 2?"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OVERLEAF_CONFIG_FILE` | `overleaf_config.json` | Path to configuration file |
| `OVERLEAF_TEMP_DIR` | `./overleaf_cache` | Local cache directory for git repos |
| `OVERLEAF_PROJECT_ID` | - | Default project ID (single-project mode) |
| `OVERLEAF_GIT_TOKEN` | - | Default git token (single-project mode) |
| `OVERLEAF_GIT_AUTHOR_NAME` | `Overleaf MCP` | Git commit author name |
| `OVERLEAF_GIT_AUTHOR_EMAIL` | `mcp@overleaf.local` | Git commit author email |

---

## How It Works

```
┌─────────────────┐     MCP Protocol     ┌─────────────────┐
│  AI Assistant   │◄───────────────────►│  Overleaf MCP   │
│ (Claude, etc.)  │                      │     Server      │
└─────────────────┘                      └────────┬────────┘
                                                  │
                                                  │ Git (HTTPS)
                                                  ▼
                                         ┌─────────────────┐
                                         │    Overleaf     │
                                         │   Git Server    │
                                         └─────────────────┘
```

1. **Clone/Pull**: Server clones or pulls the latest from Overleaf's Git endpoint
2. **Local Operations**: Read/write operations happen on local cache
3. **Commit/Push**: Changes are committed and pushed back to Overleaf
4. **Real-time Sync**: Overleaf reflects changes immediately in the web editor

---

## Security Notes

- **Tokens are sensitive**: Git tokens provide full read/write access
- **Never commit secrets**: `overleaf_config.json` is gitignored by default
- **Use environment variables**: For CI/CD or shared environments
- **Token rotation**: Regenerate tokens periodically in Overleaf settings

---

## Troubleshooting

### "No projects configured"
- Ensure `overleaf_config.json` exists and has valid JSON
- Check `OVERLEAF_CONFIG_FILE` points to the correct path

### "Permission denied" or "Read-only filesystem"
- Set `OVERLEAF_TEMP_DIR` to an absolute writable path
- Ensure the cache directory exists and is writable

### "Authentication failed"
- Verify your git token is correct
- Check if the token has expired (regenerate in Overleaf)
- Ensure you have Git integration enabled (requires paid Overleaf plan)

### "Server not appearing in Claude"
- Restart Claude Desktop completely (Cmd+Q / Ctrl+Q)
- Check the config JSON is valid (no trailing commas)
- Verify Python path is correct (use absolute path to venv)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Overleaf](https://www.overleaf.com/) for the Git integration
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [Anthropic](https://www.anthropic.com/) for Claude and the MCP SDK

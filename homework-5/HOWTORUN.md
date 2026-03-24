# How to Run - Homework 5 MCP Servers

## Prerequisites

- **Node.js** (v18+) with npm/npx
- **Python** (3.8+) with pip
- **GitHub Personal Access Token** with scopes: `repo`, `read:org`, `read:user`
- **Jira API Token** and account access
- **VS Code** with GitHub Copilot (or Claude Desktop)

## Installation Steps

### Step 1: Install Node.js Dependencies

The GitHub, Filesystem, and Jira MCP servers run via npx (no pre-installation needed):

```bash
# Verify Node.js is installed
node --version
npm --version
```

### Step 2: Install Custom MCP Server Dependencies

```bash
cd homework-5/custom-mcp-server
pip install -r requirements.txt

# Verify fastmcp is installed
pip show fastmcp
```

### Step 3: Configure GitHub Token

1. Generate a GitHub Personal Access Token:
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo`, `read:org`, `read:user`

2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:GITHUB_TOKEN = "ghp_your_token_here"
   
   # Windows CMD
   set GITHUB_TOKEN=ghp_your_token_here
   
   # Linux/Mac
   export GITHUB_TOKEN=ghp_your_token_here
   ```

### Step 4: Configure Jira Credentials

1. Generate a Jira API Token:
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Create new API token

2. Set environment variables:
   ```bash
   # Windows PowerShell
   $env:JIRA_URL = "https://yourcompany.atlassian.net"
   $env:JIRA_USERNAME = "your.email@company.com"
   $env:JIRA_API_TOKEN = "your_jira_api_token"
   
   # Windows CMD
   set JIRA_URL=https://yourcompany.atlassian.net
   set JIRA_USERNAME=your.email@company.com
   set JIRA_API_TOKEN=your_jira_api_token
   
   # Linux/Mac
   export JIRA_URL="https://yourcompany.atlassian.net"
   export JIRA_USERNAME="your.email@company.com"
   export JIRA_API_TOKEN="your_jira_api_token"
   ```

### Step 5: Configure MCP Client

#### Option A: VS Code Copilot

Add to `.vscode/settings.json`:

```json
{
  "github.copilot.chat.mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_GITHUB_TOKEN>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework"
      ]
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "mcp-server-jira"],
      "env": {
        "JIRA_URL": "<YOUR_JIRA_URL>",
        "JIRA_USERNAME": "<YOUR_JIRA_EMAIL>",
        "JIRA_API_TOKEN": "<YOUR_JIRA_TOKEN>"
      }
    },
    "lorem-ipsum": {
      "command": "python",
      "args": ["d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework/homework-5/custom-mcp-server/server.py"]
    }
  }
}
```

#### Option B: Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_GITHUB_TOKEN>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework"
      ]
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "mcp-server-jira"],
      "env": {
        "JIRA_URL": "<YOUR_JIRA_URL>",
        "JIRA_USERNAME": "<YOUR_JIRA_EMAIL>",
        "JIRA_API_TOKEN": "<YOUR_JIRA_TOKEN>"
      }
    },
    "lorem-ipsum": {
      "command": "python",
      "args": ["d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework/homework-5/custom-mcp-server/server.py"]
    }
  }
}
```

### Step 6: Restart IDE/Client

After configuration changes, restart VS Code or Claude Desktop to load the MCP servers.

## Testing Each MCP Server

### Test 1: GitHub MCP

```
Prompt: "List recent pull requests in bes422/AI-Coding-Partner-Homework"
Expected: List of PRs with titles and numbers
```

### Test 2: Filesystem MCP

```
Prompt: "List all files in the homework-5 directory"
Expected: Directory listing with file names
```

### Test 3: Jira MCP

```
Prompt: "Give me the Jira tickets of the last 5 bugs on a project"
Expected: List of 5 bug ticket numbers (e.g., PROJ-123, PROJ-456)
Note: Do not share bug descriptions (sensitive information)
```

### Test 4: Custom MCP Server

```
Prompt: "Use the read tool to get 10 words from lorem ipsum"
Expected: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do"

Prompt: "Use the read tool" (default 30 words)
Expected: First 30 words from lorem-ipsum.md
```

## Verification Checklist

- [ ] Node.js v18+ installed
- [ ] Python 3.8+ installed
- [ ] fastmcp package installed
- [ ] GitHub token configured
- [ ] Jira credentials configured
- [ ] MCP configuration added to IDE settings
- [ ] IDE restarted after configuration
- [ ] GitHub MCP returns data
- [ ] Filesystem MCP lists files
- [ ] Jira MCP returns bug tickets
- [ ] Custom `read` tool returns word-limited content

## Troubleshooting

### "MCP server not found"
- Verify npx is available: `npx --version`
- Check JSON configuration syntax
- Restart IDE after changes

### "GitHub authentication failed"
- Verify token has correct scopes
- Check token is not expired
- Ensure env variable is set

### "Jira authentication failed"
- Verify API token is correct
- Check username is your Atlassian email
- Ensure Jira URL has no trailing slash

### "Custom server won't start"
- Run `python server.py` directly to see errors
- Verify `fastmcp` is installed
- Check file paths are correct

### "Tool not appearing in Claude/Copilot"
- MCP servers load on IDE startup
- Try restarting IDE completely
- Check IDE logs for MCP errors

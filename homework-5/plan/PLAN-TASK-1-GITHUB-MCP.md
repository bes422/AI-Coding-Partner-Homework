# Plan: Task 1 - GitHub MCP Configuration

## Overview
Connect Claude/Copilot to GitHub via the official GitHub MCP server to enable AI-assisted repository interactions.

## Prerequisites
- GitHub account with repository access
- GitHub Personal Access Token (PAT) with appropriate scopes
- Node.js installed (for npx execution)

## Steps

### 1. Generate GitHub Personal Access Token
- Navigate to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate token with scopes: `repo`, `read:org`, `read:user`
- Save token securely (will be used in configuration)

### 2. Install GitHub MCP Server
The official GitHub MCP server is available via npx:
```bash
npx @modelcontextprotocol/server-github
```

### 3. Configure MCP Client
Add to `mcp.json` or `.mcp.json` in homework-5 root:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

For VS Code Copilot, add to `.vscode/settings.json`:
```json
{
  "github.copilot.chat.mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 4. Verify Configuration
- Restart IDE/Claude
- Check MCP server is registered without errors

### 5. Test Interaction
Perform one of the following:
- "List recent pull requests in bes422/AI-Coding-Partner-Homework"
- "Summarize recent commits on homework-5-submissions branch"
- "Create a test issue in my repository"

### 6. Capture Screenshots
Save to `docs/screenshots/github-mcp-result.png`:
- The MCP call request
- The successful response with data

## Success Criteria
- [ ] GitHub PAT configured with valid scopes
- [ ] MCP server starts without errors
- [ ] At least one interaction returns valid results
- [ ] Screenshot captured and saved

## Security Note
Never commit actual GitHub tokens. Use environment variables or `.env` files (add to `.gitignore`).

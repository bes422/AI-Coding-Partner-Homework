# Plan: Task 3 - Jira MCP Configuration

## Overview
Connect Claude/Copilot to Jira via the Jira MCP server to query project tickets and retrieve bug information.

## Prerequisites
- Jira account with project access
- Jira API Token
- Jira instance URL (e.g., `https://yourcompany.atlassian.net`)
- Project key for a project with bug tickets

## Steps

### 1. Generate Jira API Token
1. Navigate to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "MCP Integration")
4. Copy and save the token securely

### 2. Identify Jira Configuration Details
Required values:
- `JIRA_URL`: Your Jira instance URL (e.g., `https://yourcompany.atlassian.net`)
- `JIRA_USERNAME`: Your Atlassian account email
- `JIRA_API_TOKEN`: The generated API token
- `PROJECT_KEY`: The project key containing bugs (e.g., `PROJ`, `DEV`)

### 3. Install Jira MCP Server
Use the community Jira MCP server via npx:
```bash
npx mcp-server-jira
```

Or install Python-based version:
```bash
pip install mcp-server-jira
```

### 4. Configure MCP Client
Add to `mcp.json` or `.mcp.json` in homework-5 root:
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "mcp-server-jira"],
      "env": {
        "JIRA_URL": "https://yourcompany.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "<YOUR_API_TOKEN>"
      }
    }
  }
}
```

For VS Code Copilot, add to `.vscode/settings.json`:
```json
{
  "github.copilot.chat.mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "mcp-server-jira"],
      "env": {
        "JIRA_URL": "https://yourcompany.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "<YOUR_API_TOKEN>"
      }
    }
  }
}
```

### 5. Verify Configuration
- Restart IDE/Claude
- Check MCP server is registered without errors
- Verify connection to Jira instance

### 6. Execute Required Request
Make this exact request as specified in TASKS.md:
> "Give me the Jira tickets of the last 5 bugs on a project"

This will use JQL query like:
```
project = <PROJECT_KEY> AND type = Bug ORDER BY created DESC
```

### 7. Capture Screenshots
Save to `docs/screenshots/jira-mcp-result.png`:
- The MCP call request
- Response showing ticket numbers (e.g., PROJ-123, PROJ-456, etc.)

**IMPORTANT:** Do NOT include bug descriptions in screenshots (sensitive information). Only show ticket numbers to represent the working response.

## Success Criteria
- [ ] Jira API token generated with valid access
- [ ] Jira MCP server configured in mcp.json
- [ ] MCP server starts without errors
- [ ] Query for last 5 bugs returns valid ticket numbers
- [ ] Screenshot captured showing ticket numbers only (no sensitive descriptions)

## Security Notes
- Never commit Jira credentials to version control
- Use environment variables or `.env` files
- Add `.env` to `.gitignore`
- Consider using credential managers for production use

## Troubleshooting

### Authentication Failed
- Verify API token is correct and not expired
- Check username is your Atlassian email
- Ensure Jira URL has no trailing slash

### No Results Returned
- Verify project key exists
- Check user has access to the project
- Confirm bugs exist in the project with type "Bug"

### MCP Server Won't Start
- Check Node.js is installed for npx version
- Verify all environment variables are set
- Check network access to Jira instance

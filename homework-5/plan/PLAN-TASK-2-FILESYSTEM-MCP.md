# Plan: Task 2 - Filesystem MCP Configuration

## Overview
Connect Claude/Copilot to a local directory via the Filesystem MCP server to enable AI-assisted file operations.

## Prerequisites
- Node.js installed (for npx execution)
- Target directory path identified

## Steps

### 1. Identify Target Directory
Use the homework repository folder:
```
d:\projects\ai_coding_partner_homework\AI-Coding-Partner-Homework
```

### 2. Install Filesystem MCP Server
The official Filesystem MCP server is available via npx:
```bash
npx @modelcontextprotocol/server-filesystem <path>
```

### 3. Configure MCP Client
Add to `mcp.json` or `.mcp.json` in homework-5 root:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework"
      ]
    }
  }
}
```

For VS Code Copilot, add to `.vscode/settings.json`:
```json
{
  "github.copilot.chat.mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework"
      ]
    }
  }
}
```

### 4. Verify Configuration
- Restart IDE/Claude
- Check MCP server is registered without errors

### 5. Test Interaction
Perform one of the following:
- "List all files in the homework-5 directory"
- "Read the contents of homework-5/TASKS.md"
- "Summarize the directory structure of this project"

### 6. Capture Screenshots
Save to `docs/screenshots/filesystem-mcp-result.png`:
- The MCP call request
- The successful response showing file data

## Success Criteria
- [ ] Valid directory path configured
- [ ] MCP server starts without errors
- [ ] At least one file/directory interaction succeeds
- [ ] Screenshot captured and saved

## Path Format Note
On Windows, use forward slashes (`/`) in JSON paths or escape backslashes (`\\`).

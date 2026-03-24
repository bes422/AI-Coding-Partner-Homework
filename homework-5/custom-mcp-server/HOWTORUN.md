# Custom MCP Server - How to Run

## Overview

This is a custom MCP server built with FastMCP that reads from `lorem-ipsum.md` and returns word-limited content.

### Key Concepts

- **Resources**: URIs that Claude can read from (e.g., files, APIs). This server exposes:
  - `lorem://content` - Returns 30 words (default)
  - `lorem://content/{word_count}` - Returns specified number of words

- **Tools**: Actions Claude can call to perform operations. This server exposes:
  - `read(word_count=30)` - Returns word-limited content from lorem-ipsum.md

## Installation

### 1. Navigate to the custom-mcp-server directory

```bash
cd homework-5/custom-mcp-server
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify FastMCP installation

```bash
pip show fastmcp
```

## Running the Server

### Standalone Test

```bash
python server.py
```

### With FastMCP CLI (if available)

```bash
fastmcp run server.py
```

## MCP Configuration

### Option 1: Project-level configuration

Add to `homework-5/mcp.json`:

```json
{
  "mcpServers": {
    "lorem-ipsum": {
      "command": "python",
      "args": ["custom-mcp-server/server.py"],
      "cwd": "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework/homework-5"
    }
  }
}
```

### Option 2: VS Code Copilot configuration

Add to `.vscode/settings.json`:

```json
{
  "github.copilot.chat.mcpServers": {
    "lorem-ipsum": {
      "command": "python",
      "args": ["d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework/homework-5/custom-mcp-server/server.py"]
    }
  }
}
```

## Testing the `read` Tool

After configuring, test in Claude/Copilot chat:

| Request | Expected Result |
|---------|-----------------|
| "Use the read tool" | Returns 30 words (default) |
| "Use the read tool to get 10 words" | Returns exactly 10 words |
| "Read 50 words from lorem ipsum" | Returns exactly 50 words |

### Example Responses

**Default (30 words):**
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
nostrud exercitation ullamco laboris
```

**10 words:**
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
```

## Verification Checklist

- [ ] `pip install -r requirements.txt` succeeds
- [ ] `python server.py` starts without errors
- [ ] MCP configuration points to correct path
- [ ] `read` tool returns expected word count
- [ ] Resource URI `lorem://content` is accessible

## Troubleshooting

### Server won't start
- Ensure Python 3.8+ is installed
- Verify `fastmcp` is installed: `pip show fastmcp`
- Check file paths are correct

### Tool not found in Claude/Copilot
- Restart the IDE after configuration changes
- Verify MCP configuration JSON is valid
- Check the server is running without errors

### Wrong word count returned
- The `word_count` parameter accepts integers only
- Default is 30 if not specified

# How to Run: Custom MCP Server (Lorem Ipsum)

## Overview

This custom MCP server is built with [FastMCP](https://github.com/jlowin/fastmcp). It exposes:

- **Resource** `lorem://content/{word_count}` — reads `lorem-ipsum.md` and returns the first N words.
- **Tool** `read(word_count=30)` — Claude calls this tool to retrieve word-limited content from the resource.

---

## 1. Install Dependencies

From the `custom-mcp-server/` directory:

```bash
pip install -r requirements.txt
```

This installs `fastmcp` and its dependencies.

> **Python 3.9+** is required.

---

## 2. Run the Server

```bash
python server.py
```

The server starts and listens for MCP connections via stdio (the default FastMCP transport).

Expected output:
```
Starting Lorem Ipsum Server...
```

---

## 3. Connect MCP Configuration

Add the following entry to your `mcp.json` (or `.mcp.json`) at the root of `homework-5/`:

```json
{
  "mcpServers": {
    "lorem-ipsum": {
      "command": "python",
      "args": ["custom-mcp-server/server.py"]
    }
  }
}
```

For **Claude Code** (CLI), place `mcp.json` in the `homework-5/` directory and run Claude from there, or add the server via:

```bash
claude mcp add lorem-ipsum python custom-mcp-server/server.py
```

For **VS Code Copilot**, add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "lorem-ipsum": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/homework-5/custom-mcp-server/server.py"]
    }
  }
}
```

---

## 4. Use / Test the `read` Tool

Once connected, ask Claude:

```
Use the read tool to get the first 30 words from the Lorem Ipsum server.
```

Or with a custom word count:

```
Use the read tool with word_count=10 to get 10 words.
```

Expected response (30 words):
```
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi
```

You can also access the resource directly by URI:

```
Read the resource lorem://content/50
```

---

## 5. Verify `fastmcp` Dependency

```bash
pip show fastmcp
```

Should output package info including the version.

---

## File Structure

```
custom-mcp-server/
├── server.py           # FastMCP server implementation
├── lorem-ipsum.md      # Source text (100+ words)
├── requirements.txt    # Dependencies: fastmcp>=0.1.0
└── HOWTORUN.md         # This file
```

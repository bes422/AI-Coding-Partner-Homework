# Homework 5: Configure MCP Servers

**Author:** bes422

---

## Overview

This homework configures three external MCP servers (GitHub, Filesystem, and a GitHub Issues query as a Jira alternative) and builds one custom MCP server using FastMCP.

---

## Task 1: GitHub MCP

**What was done:**
Configured the official `@modelcontextprotocol/server-github` MCP server in `mcp.json`. The server is authenticated via a `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable (PAT with `repo`, `read:org`, `read:user` scopes). Performed an interaction listing recent pull requests in the `bes422/AI-Coding-Partner-Homework` repository.

**Configuration:**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

**Screenshot:** `docs/screenshots/github-mcp-result.png`

---

## Task 2: Filesystem MCP

**What was done:**
Configured the official `@modelcontextprotocol/server-filesystem` MCP server in `mcp.json` pointing to the current directory (`.`). Performed an interaction to list all files in the `homework-5` directory and read `TASKS.md`.

**Configuration:**
```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
}
```

**Screenshot:** `docs/screenshots/filesystem-mcp-result.png`

---

## Task 3: Project Management MCP (GitHub Issues)

**Note:** Jira was not available for this project. GitHub Issues via the GitHub MCP server was used as an equivalent demonstration of project management integration. The same concepts apply — querying tickets/issues by type, retrieving recent items, and AI-assisted project management queries.

**What was done:**
Used the already-configured GitHub MCP server (Task 1) to query GitHub Issues. Created 10 demo issues in the repository (8 labeled `bug`, 2 labeled `enhancement`). Executed the equivalent of the Jira request:

> *"Give me the last 5 issues labeled 'bug' in bes422/AI-Coding-Partner-Homework"*

This returned issue numbers demonstrating the integration.

| Jira Concept | GitHub Issues Equivalent |
|---|---|
| MCP Server | `@modelcontextprotocol/server-github` (reused) |
| Bug query | `label:bug` filter via GitHub API |
| Ticket numbers | GitHub Issue numbers (#1, #2, ...) |

**Screenshot:** `docs/screenshots/github-issues-mcp-result.png`

---

## Task 4: Custom MCP Server with FastMCP

**What was done:**
Built a custom MCP server in `custom-mcp-server/` using FastMCP. The server exposes:

- **Resource** `lorem://content/{word_count}` — reads `lorem-ipsum.md` and returns the first N words.
- **Tool** `read(word_count=30)` — Claude calls this to retrieve word-limited content.

### Concepts

**Resources** are URIs that Claude can read from (e.g., files, APIs, databases). They are defined with a URI pattern and accessed like files — Claude fetches the content by addressing the URI.

**Tools** are actions Claude can call to perform operations (e.g., reading a file, running a command, querying an API). Tools are invoked by name with typed arguments and return structured results.

**Screenshot:** `docs/screenshots/custom-mcp-read-tool-result.png`

**Setup instructions:** See [`custom-mcp-server/HOWTORUN.md`](custom-mcp-server/HOWTORUN.md)

---

## Project Structure

```
homework-5/
├── README.md                          ← This file
├── TASKS.md                           ← Assignment description
├── mcp.json                           ← MCP server configuration
├── custom-mcp-server/
│   ├── server.py                      ← FastMCP implementation
│   ├── lorem-ipsum.md                 ← Source text for resource output
│   ├── requirements.txt               ← Dependencies (includes fastmcp)
│   └── HOWTORUN.md                    ← Install, run, connect, and usage guide
├── plan/
│   ├── PLAN-TASK-1-GITHUB-MCP.md
│   ├── PLAN-TASK-2-FILESYSTEM-MCP.md
│   ├── PLAN-TASK-3-GITHUB-ISSUES.md
│   └── PLAN-TASK-4-CUSTOM-MCP.md
└── docs/
    └── screenshots/
        ├── github-mcp-result.png
        ├── filesystem-mcp-result.png
        ├── github-issues-mcp-result.png
        └── custom-mcp-read-tool-result.png
```

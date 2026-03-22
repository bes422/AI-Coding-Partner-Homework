# Homework 5: MCP Servers Configuration

## Author
**Name:** [Your Name Here]

## Overview

This homework demonstrates the configuration and usage of Model Context Protocol (MCP) servers to extend AI assistant capabilities. Four MCP integrations are implemented:

| Task | MCP Server | Purpose |
|------|------------|---------|
| 1 | GitHub MCP | Repository interactions (PRs, commits, issues) |
| 2 | Filesystem MCP | Local file and directory operations |
| 3 | Jira MCP | Query Jira project tickets |
| 4 | Custom FastMCP | Custom server with `read` tool |

## Project Structure

```
homework-5/
├── README.md                    # This file
├── HOWTORUN.md                  # Installation and setup instructions
├── TASKS.md                     # Assignment requirements
├── mcp.json                     # MCP server configuration
├── custom-mcp-server/           # Task 4: Custom MCP implementation
│   ├── server.py                # FastMCP server code
│   ├── lorem-ipsum.md           # Source text for read tool
│   ├── requirements.txt         # Python dependencies
│   └── HOWTORUN.md              # Custom server instructions
├── plan/                        # Implementation plans
│   ├── PLAN-TASK-1-GITHUB-MCP.md
│   ├── PLAN-TASK-2-FILESYSTEM-MCP.md
│   ├── PLAN-TASK-3-JIRA-MCP.md
│   └── PLAN-TASK-4-CUSTOM-MCP.md
└── docs/
    └── screenshots/             # MCP call result screenshots
        ├── github-mcp-result.png
        ├── filesystem-mcp-result.png
        ├── jira-mcp-result.png
        └── custom-mcp-read-tool-result.png
```

## Task Summaries

### Task 1: GitHub MCP ⭐

Connected to GitHub via the official `@modelcontextprotocol/server-github` MCP server.

**Demonstrated interaction:** List recent pull requests / commits / create issue

**Screenshot:** [github-mcp-result.png](docs/screenshots/github-mcp-result.png)

---

### Task 2: Filesystem MCP ⭐

Connected to local filesystem via `@modelcontextprotocol/server-filesystem` MCP server.

**Demonstrated interaction:** List files / read file contents

**Screenshot:** [filesystem-mcp-result.png](docs/screenshots/filesystem-mcp-result.png)

---

### Task 3: Jira MCP ⭐⭐

Connected to Jira via `mcp-server-jira` to query project tickets.

**Required Request:** "Give me the Jira tickets of the last 5 bugs on a project"

**Response:** Ticket numbers only (no sensitive bug descriptions)

**Screenshot:** [jira-mcp-result.png](docs/screenshots/jira-mcp-result.png)

---

### Task 4: Custom MCP Server with FastMCP ⭐⭐⭐

Built a custom MCP server that reads from `lorem-ipsum.md` with word count limiting.

**Features:**
- **Resource URI:** `lorem://content/{word_count}` - reads word-limited content
- **Tool:** `read(word_count=30)` - returns specified number of words

**Key Concepts:**
- **Resources:** URIs that Claude can read from (e.g., files, APIs)
- **Tools:** Actions Claude can call to perform operations

**Screenshot:** [custom-mcp-read-tool-result.png](docs/screenshots/custom-mcp-read-tool-result.png)

## Quick Start

See [HOWTORUN.md](HOWTORUN.md) for complete setup instructions.

```bash
# 1. Install custom server dependencies
cd homework-5/custom-mcp-server
pip install -r requirements.txt

# 2. Test custom server
python server.py

# 3. Configure MCP in your IDE (see mcp.json)
```

## Technologies Used

- **MCP Protocol:** Model Context Protocol for AI tool integration
- **FastMCP:** Python framework for building MCP servers
- **Node.js/npx:** For running official MCP servers
- **Python 3.8+:** Custom server implementation

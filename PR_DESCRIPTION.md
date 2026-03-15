# 📝 Homework Submission - Homework 5

> **Student Name**: Mykhailo Bestiuk
> **Date Submitted**: March 15, 2026
> **Assignment**: Homework 5: Configure MCP Servers (GitHub, Filesystem, Jira, Custom)

---

## ✅ Summary

This PR submits the configuration of **three external MCP servers** (GitHub, Filesystem, and GitHub Issues as a Jira alternative) and a **custom MCP server** built with FastMCP that exposes a resource URI and a `read` tool for word-limited content delivery.

**Folder**: `homework-5/`

### 📦 Deliverables

| # | Deliverable | Status |
|---|------------|--------|
| 1 | GitHub MCP — configured with PAT, interaction documented | ✅ Complete |
| 2 | Filesystem MCP — configured with directory path, interaction documented | ✅ Complete |
| 3 | GitHub Issues MCP (Jira alternative) — last 5 bug issues queried | ✅ Complete |
| 4 | Custom FastMCP server — `server.py`, resource URI, `read` tool | ✅ Complete |
| 5 | `lorem-ipsum.md` — 140-word source text for resource output | ✅ Complete |
| 6 | `requirements.txt` — includes `fastmcp>=0.1.0` | ✅ Complete |
| 7 | `HOWTORUN.md` — install, run, connect, and usage instructions | ✅ Complete |
| 8 | `mcp.json` — combined config for all three server types | ✅ Complete |
| 9 | `README.md` — author, task descriptions, project structure | ✅ Complete |
| 10 | Screenshots (4 files in `docs/screenshots/`) | ✅ Complete |

---

## 🔌 Task 1: GitHub MCP

**Server**: `@modelcontextprotocol/server-github` (via npx)

**Configuration** (`mcp.json`):
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
}
```

**Interaction**: Listed recent pull requests in `bes422/AI-Coding-Partner-Homework` using the `list_pull_requests` tool.

**Screenshot**: `docs/screenshots/github-mcp-result.png`

---

## 📁 Task 2: Filesystem MCP

**Server**: `@modelcontextprotocol/server-filesystem` (via npx)

**Configuration** (`mcp.json`):
```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
}
```

**Interaction**: Listed all files in `homework-5/` and read `TASKS.md` via the filesystem MCP tools.

**Screenshot**: `docs/screenshots/filesystem-mcp-result.png`

---

## 🎫 Task 3: GitHub Issues MCP (Jira Alternative)

> **Note:** Jira was not available for this project. GitHub Issues via the GitHub MCP server was used as an equivalent demonstration of project management integration. The same concepts apply — querying tickets/issues by type, retrieving recent items, and AI-assisted project management queries.

**Interaction**: Queried the last 5 issues labeled `bug` in `bes422/AI-Coding-Partner-Homework`:

| Concept | Jira | GitHub Issues |
|---------|------|---------------|
| MCP Server | `mcp-server-jira` | `@modelcontextprotocol/server-github` |
| Bug filter | `type = Bug` | `label:bug` |
| Ticket ID | `PROJ-123` | `#1`, `#2`, ... |

**Screenshot**: `docs/screenshots/github-issues-mcp-result.png`

---

## 🛠️ Task 4: Custom MCP Server (FastMCP)

**Location**: `homework-5/custom-mcp-server/`

### What was built

| Component | Description |
|-----------|-------------|
| **Resource** `lorem://content/{word_count}` | Reads `lorem-ipsum.md`, returns first N words |
| **Tool** `read(word_count=30)` | Claude calls this to retrieve word-limited content |
| `lorem-ipsum.md` | 140-word source text |
| `requirements.txt` | `fastmcp>=0.1.0` |
| `HOWTORUN.md` | Full setup, run, connect, and usage guide |

### Key concepts documented

- **Resources**: URIs that Claude can read from (e.g., files, APIs, databases). They represent data sources accessed by URI pattern.
- **Tools**: Actions Claude can call to perform operations (e.g., reading a file, querying an API). Invoked by name with typed arguments.

### Server implementation (`server.py`)

```python
@mcp.resource("lorem://content/{word_count}")
def lorem_resource(word_count: int = 30) -> str:
    return _get_words(word_count)

@mcp.tool()
def read(word_count: int = 30) -> str:
    return _get_words(word_count)
```

**Screenshot**: `docs/screenshots/custom-mcp-read-tool-result.png`

---

## 📁 Project Structure

```
homework-5/
├── README.md                          ← Author info + task descriptions
├── TASKS.md                           ← Assignment description
├── mcp.json                           ← Combined MCP config (GitHub + Filesystem + Custom)
├── custom-mcp-server/
│   ├── server.py                      ← FastMCP server (resource + read tool)
│   ├── lorem-ipsum.md                 ← 140-word source text
│   ├── requirements.txt               ← fastmcp>=0.1.0
│   └── HOWTORUN.md                    ← Install/run/connect/usage instructions
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

---

## 📸 Screenshots

### Task 1: GitHub MCP Result
![GitHub MCP Result](homework-5/docs/screenshots/github-mcp-result.png)

### Task 2: Filesystem MCP Result
![Filesystem MCP Result](homework-5/docs/screenshots/filesystem-mcp-result.png)

### Task 3: GitHub Issues MCP Result
![GitHub Issues MCP Result](homework-5/docs/screenshots/github-issues-mcp-result.png)

### Task 4: Custom MCP Read Tool Result
![Custom MCP Read Tool Result](homework-5/docs/screenshots/custom-mcp-read-tool-result.png)

---

## 🤖 AI Tools Used

- **Claude Code CLI** (claude-sonnet-4-6) — MCP server configuration, custom server implementation, documentation
- **FastMCP** — Python framework for building MCP servers

---

## 🚀 How to Run the Custom MCP Server

```bash
cd homework-5/custom-mcp-server
pip install -r requirements.txt
python server.py
```

See [`custom-mcp-server/HOWTORUN.md`](homework-5/custom-mcp-server/HOWTORUN.md) for full instructions including MCP client configuration.

---

**Ready for review!** 🚀

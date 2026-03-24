# Plan: Task 4 - Custom MCP Server with FastMCP

## Overview
Build a custom MCP server using FastMCP that exposes a resource URI and a `read` tool to return word-limited content from `lorem-ipsum.md`.

## Folder Structure
```
homework-5/
└── custom-mcp-server/
    ├── server.py           # FastMCP implementation
    ├── lorem-ipsum.md      # Source text file
    ├── requirements.txt    # Dependencies (must include fastmcp)
    └── HOWTORUN.md         # Setup instructions
```

## Steps

### 1. Create `custom-mcp-server/` Directory
Create folder under `homework-5/`.

### 2. Create `requirements.txt`
```
fastmcp>=0.1.0
```

### 3. Create `lorem-ipsum.md`
Add lorem ipsum source text (100+ words for testing):
```markdown
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt 
in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium 
tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo 
pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.
```

### 4. Create `server.py`
```python
"""Custom MCP Server using FastMCP.

This server provides:
- A Resource URI that reads from lorem-ipsum.md with word_count parameter
- A Tool named 'read' that returns word-limited content

Concepts:
- Resources: URIs that Claude can read from (e.g., files, APIs)
- Tools: Actions Claude can call to perform operations
"""
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Lorem Ipsum Server")

# Path to the source file
LOREM_FILE = Path(__file__).parent / "lorem-ipsum.md"


def get_words(word_count: int = 30) -> str:
    """Read lorem-ipsum.md and return exactly word_count words."""
    if not LOREM_FILE.exists():
        return f"Error: {LOREM_FILE} not found"
    
    content = LOREM_FILE.read_text(encoding="utf-8")
    words = content.split()
    limited_words = words[:word_count]
    return " ".join(limited_words)


@mcp.resource("lorem://content/{word_count}")
def lorem_resource(word_count: int = 30) -> str:
    """Resource URI that returns word-limited content from lorem-ipsum.md.
    
    Args:
        word_count: Number of words to return (default: 30)
    
    Returns:
        String containing exactly word_count words from lorem-ipsum.md
    """
    return get_words(word_count)


@mcp.tool()
def read(word_count: int = 30) -> str:
    """Read content from lorem-ipsum.md with a word limit.
    
    Args:
        word_count: Number of words to return (default: 30)
    
    Returns:
        String containing exactly word_count words from the file
    """
    return get_words(word_count)


if __name__ == "__main__":
    mcp.run()
```

### 5. Create `HOWTORUN.md` in custom-mcp-server/
See separate file for full instructions.

### 6. Update Main MCP Configuration
Create `homework-5/mcp.json` combining all servers:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "lorem-ipsum": {
      "command": "python",
      "args": ["custom-mcp-server/server.py"]
    }
  }
}
```

### 7. Test Custom Server
- Verify server starts: `python custom-mcp-server/server.py`
- Test `read` tool with default word_count (30)
- Test `read` tool with custom word_count (10, 50)
- Verify resource URI works

### 8. Capture Screenshots
Save to `docs/screenshots/custom-mcp-read-tool-result.png`:
- The `read` tool call
- Response showing word-limited content

## Success Criteria
- [ ] `server.py` implements FastMCP correctly
- [ ] `lorem-ipsum.md` exists with source text
- [ ] `requirements.txt` includes `fastmcp`
- [ ] `HOWTORUN.md` documents setup completely
- [ ] Server starts without errors
- [ ] `read` tool returns correct word count
- [ ] Resource URI functions correctly
- [ ] Screenshots captured

## Key Implementation Details

### FastMCP Decorators
- `@mcp.resource("uri://pattern/{param}")` - Defines a resource
- `@mcp.tool()` - Defines a callable tool

### Word Limiting Logic
```python
words = content.split()[:word_count]
return " ".join(words)
```

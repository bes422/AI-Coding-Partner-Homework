"""Custom MCP Server using FastMCP.

This server provides:
- A Resource URI that reads from lorem-ipsum.md with a word_count parameter
- A Tool named 'read' that returns word-limited content from the resource

Concepts:
- Resources: URIs that Claude can read from (e.g., files, APIs, databases).
  They represent data sources that Claude accesses by URI pattern.
- Tools: Actions Claude can call to perform operations (e.g., reading a file,
  running a command, querying an API). Tools are invoked by name with arguments.
"""

from pathlib import Path

from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Lorem Ipsum Server")

# Path to the source file (relative to this script)
LOREM_FILE = Path(__file__).parent / "lorem-ipsum.md"


def _get_words(word_count: int = 30) -> str:
    """Read lorem-ipsum.md and return exactly word_count words."""
    if not LOREM_FILE.exists():
        return f"Error: {LOREM_FILE} not found"

    content = LOREM_FILE.read_text(encoding="utf-8")
    words = content.split()
    return " ".join(words[:word_count])


@mcp.resource("lorem://content/{word_count}")
def lorem_resource(word_count: int = 30) -> str:
    """Resource URI that returns word-limited content from lorem-ipsum.md.

    URI pattern: lorem://content/{word_count}

    Args:
        word_count: Number of words to return (default: 30)

    Returns:
        String containing exactly word_count words from lorem-ipsum.md
    """
    return _get_words(word_count)


@mcp.tool()
def read(word_count: int = 30) -> str:
    """Read content from lorem-ipsum.md with a word limit.

    Args:
        word_count: Number of words to return (default: 30)

    Returns:
        String containing exactly word_count words from the file
    """
    return _get_words(word_count)


if __name__ == "__main__":
    mcp.run()

"""Custom MCP Server using FastMCP.

This server provides:
- A Resource URI that reads from lorem-ipsum.md with word_count parameter
- A Tool named 'read' that returns word-limited content

Concepts:
- Resources: URIs that Claude can read from (e.g., files, APIs).
  They represent data sources that can be accessed via URI patterns.
- Tools: Actions Claude can call to perform operations (e.g., reading 
  a file, running a command). They are callable functions with parameters.
"""
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Lorem Ipsum Server")

# Path to the source file
LOREM_FILE = Path(__file__).parent / "lorem-ipsum.md"


def get_words(word_count: int = 30) -> str:
    """Read lorem-ipsum.md and return exactly word_count words.
    
    Args:
        word_count: Number of words to return (default: 30)
    
    Returns:
        String containing exactly word_count words from lorem-ipsum.md
    """
    if not LOREM_FILE.exists():
        return f"Error: {LOREM_FILE} not found"
    
    content = LOREM_FILE.read_text(encoding="utf-8")
    words = content.split()
    limited_words = words[:word_count]
    return " ".join(limited_words)


@mcp.resource("lorem://content")
def lorem_resource_default() -> str:
    """Resource URI that returns 30 words (default) from lorem-ipsum.md.
    
    Returns:
        String containing 30 words from lorem-ipsum.md
    """
    return get_words(30)


@mcp.resource("lorem://content/{word_count}")
def lorem_resource(word_count: int) -> str:
    """Resource URI that returns word-limited content from lorem-ipsum.md.
    
    Args:
        word_count: Number of words to return
    
    Returns:
        String containing exactly word_count words from lorem-ipsum.md
    """
    return get_words(int(word_count))


@mcp.tool()
def read(word_count: int = 30) -> str:
    """Read content from lorem-ipsum.md with a word limit.
    
    This tool reads the lorem-ipsum.md file and returns exactly
    the specified number of words from it.
    
    Args:
        word_count: Number of words to return (default: 30)
    
    Returns:
        String containing exactly word_count words from the file
    """
    return get_words(word_count)


if __name__ == "__main__":
    mcp.run()

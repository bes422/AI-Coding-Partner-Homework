"""MCP stdio test client using FastMCP's built-in client.

Usage:
    python test_mcp.py custom    # test custom lorem-ipsum server
    python test_mcp.py filesystem # test filesystem MCP server
    python test_mcp.py github    # test GitHub MCP server
    python test_mcp.py jira      # test Jira MCP server
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from fastmcp import Client


def _extract_text(result) -> str:
    """Extract text from FastMCP tool/resource call result."""
    if result is None:
        return ""
    # CallToolResult has a .content list
    if hasattr(result, "content"):
        parts = [c.text for c in result.content if hasattr(c, "text")]
        return "\n".join(parts)
    # ResourceContent list
    if isinstance(result, list):
        parts = [c.text for c in result if hasattr(c, "text")]
        return "\n".join(parts)
    return str(result)


async def test_custom_server():
    server_path = Path(__file__).parent / "server.py"
    print("=" * 60)
    print("CUSTOM MCP SERVER (FastMCP - Lorem Ipsum)")
    print("=" * 60)
    print(f"Server: {server_path}")
    print()

    async with Client(str(server_path)) as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        print()

        # Call read with default word count (30)
        print(">>> Tool call: read()")
        result = await client.call_tool("read", {})
        content = _extract_text(result)
        print(f"Response:\n{content}")
        print()

        # Call read with custom word count
        print(">>> Tool call: read(word_count=10)")
        result = await client.call_tool("read", {"word_count": 10})
        content = _extract_text(result)
        print(f"Response:\n{content}")
        print()

        # List resources
        resources = await client.list_resources()
        print(f"Available resources: {[str(r.uri) for r in resources]}")
        print()

        # Read default resource
        print(">>> Resource read: lorem://content")
        resource_result = await client.read_resource("lorem://content")
        content = _extract_text(resource_result)
        print(f"Response:\n{content}")

    print()
    print("[OK] Custom MCP server test complete")


async def test_filesystem_server():
    homework_path = "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework"
    print("=" * 60)
    print("FILESYSTEM MCP SERVER")
    print("=" * 60)
    print(f"Allowed path: {homework_path}")
    print()

    server_config = {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", homework_path],
            }
        }
    }

    async with Client(server_config) as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        print()

        # List the homework-5 directory
        target = "d:/projects/ai_coding_partner_homework/AI-Coding-Partner-Homework/homework-5"
        print(f">>> Tool call: list_directory({target})")
        result = await client.call_tool("list_directory", {"path": target})
        content = _extract_text(result)
        print(f"Response:\n{content}")

    print()
    print("[OK] Filesystem MCP server test complete")


async def test_github_server():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("[ERROR] GITHUB_TOKEN environment variable not set")
        return

    print("=" * 60)
    print("GITHUB MCP SERVER")
    print("=" * 60)
    print()

    server_config = {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": token},
            }
        }
    }

    async with Client(server_config) as client:
        tools = await client.list_tools()
        print(f"Available tools ({len(tools)} total): {[t.name for t in tools[:5]]}...")
        print()

        # Search repositories
        print(">>> Tool call: search_repositories(query='AI-Coding-Partner-Homework')")
        result = await client.call_tool(
            "search_repositories",
            {"query": "AI-Coding-Partner-Homework"},
        )
        content = _extract_text(result)
        if len(content) > 1500:
            content = content[:1500] + "\n... (truncated)"
        print(f"Response:\n{content}")

    print()
    print("[OK] GitHub MCP server test complete")


async def test_jira_server():
    jira_url = os.environ.get("JIRA_URL", "")
    jira_user = os.environ.get("JIRA_USERNAME", "")
    jira_token = os.environ.get("JIRA_API_TOKEN", "")

    if not all([jira_url, jira_user, jira_token]):
        missing = [k for k, v in [("JIRA_URL", jira_url), ("JIRA_USERNAME", jira_user), ("JIRA_API_TOKEN", jira_token)] if not v]
        print(f"[ERROR] Missing Jira env vars: {missing}")
        return

    print("=" * 60)
    print("JIRA MCP SERVER")
    print("=" * 60)
    print(f"Jira URL: {jira_url}")
    print()

    # mcp-server-jira (Python) uses --jira-base-url and --jira-token CLI args
    server_config = {
        "mcpServers": {
            "jira": {
                "command": "python",
                "args": [
                    "-m", "mcp_server_jira",
                    "--jira-base-url", jira_url.rstrip("/"),
                    "--jira-token", jira_token,
                ],
            }
        }
    }

    async with Client(server_config) as client:
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        print()

        # Search for last 5 bug tickets
        print(">>> Tool call: search_issues (issuetype = Bug ORDER BY created DESC, max 5)")
        result = await client.call_tool(
            "search_issues",
            {"jql": "issuetype = Bug ORDER BY created DESC", "max_results": 5},
            raise_on_error=False,
        )

        content = _extract_text(result)
        if len(content) > 3000:
            content = content[:3000] + "\n... (truncated)"
        print(f"Response:\n{content}")

    print()
    print("[OK] Jira MCP server test complete")


async def main():
    server = sys.argv[1] if len(sys.argv) > 1 else "custom"

    if server == "custom":
        await test_custom_server()
    elif server == "filesystem":
        await test_filesystem_server()
    elif server == "github":
        await test_github_server()
    elif server == "jira":
        await test_jira_server()
    else:
        print(f"Unknown server: {server}")
        print("Usage: python test_mcp.py [custom|filesystem|github|jira]")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

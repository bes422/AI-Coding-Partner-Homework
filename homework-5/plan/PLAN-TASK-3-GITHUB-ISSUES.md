# Plan: Task 3 - GitHub Issues MCP (Alternative to Jira)

## Overview
Instead of Jira, use the GitHub MCP server (already configured in Task 1) to query GitHub Issues, demonstrating the same project management integration concepts.

## Why This Works
- GitHub Issues serves same purpose as Jira tickets
- Uses same MCP server from Task 1 (no additional setup)
- Can query by label (e.g., "bug") just like Jira issue types
- Demonstrates equivalent AI-assisted ticket querying

## Prerequisites
- GitHub MCP already configured (Task 1)
- GitHub account with access to bes422/AI-Coding-Partner-Homework repository

## Preconditions

### Create 10 Demo Issues
Before testing, create 10 demo issues in the repository:

1. Go to: https://github.com/bes422/AI-Coding-Partner-Homework/issues
2. Create 10 issues with the following pattern:

| # | Title | Label |
|---|-------|-------|
| 1 | [Bug] Login page not loading on mobile | bug |
| 2 | [Bug] Search results return duplicate items | bug |
| 3 | [Bug] Date picker shows wrong timezone | bug |
| 4 | [Bug] Export to CSV missing headers | bug |
| 5 | [Bug] Session timeout too short | bug |
| 6 | [Feature] Add dark mode support | enhancement |
| 7 | [Bug] Form validation error message unclear | bug |
| 8 | [Feature] Add keyboard shortcuts | enhancement |
| 9 | [Bug] Image upload fails for PNG files | bug |
| 10 | [Bug] Pagination breaks on last page | bug |

**Result:** 8 issues labeled "bug", 2 labeled "enhancement"

## Steps

### 1. Verify Demo Issues Exist
- Go to: https://github.com/bes422/AI-Coding-Partner-Homework/issues
- Confirm 10 issues are created (8 with "bug" label)
- Filter by label: https://github.com/bes422/AI-Coding-Partner-Homework/issues?q=label%3Abug

### 2. Use Existing GitHub MCP Configuration
No additional configuration needed - reuse Task 1's setup in `mcp.json`:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 3. Execute Equivalent Request
Modify the original Jira request to GitHub context:

**Original Jira request:**
> "Give me the Jira tickets of the last 5 bugs on a project"

**Equivalent GitHub request:**
> "Give me the last 5 issues labeled 'bug' in bes422/AI-Coding-Partner-Homework"

Or if no bug label exists:
> "Give me the last 5 issues in bes422/AI-Coding-Partner-Homework"

### 4. Capture Screenshots
Save to `docs/screenshots/github-issues-mcp-result.png`:
- The MCP call request for issues
- Response showing issue numbers (e.g., #1, #2, #3)
- Show this is separate from Task 1's interaction

### 5. Document the Alternative
In README.md, note:
```markdown
### Task 3: Project Management MCP (GitHub Issues)

**Note:** Jira was not available, so GitHub Issues via GitHub MCP 
was used as an equivalent demonstration of project management 
integration. The same concepts apply:
- Querying tickets/issues by type
- Retrieving recent items
- AI-assisted project management queries
```

## Success Criteria
- [ ] 10 demo issues created in repository
- [ ] GitHub MCP configured (from Task 1)
- [ ] Query for last 5 issues/bugs returns valid results
- [ ] Screenshot shows issue numbers
- [ ] Documentation explains the alternative choice

## Comparison: Jira vs GitHub Issues

| Aspect | Jira | GitHub Issues |
|--------|------|---------------|
| MCP Server | mcp-server-jira | @modelcontextprotocol/server-github |
| Query Type | JQL (Jira Query Language) | GitHub API filters |
| Bug Filter | `type = Bug` | `label:bug` |
| Concept Demonstrated | Project management integration | ✓ Same |

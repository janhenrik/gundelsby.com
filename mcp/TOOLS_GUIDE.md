# MCP Server Tools Guide

## Why Multiple Tools?

Previously, the server only had a `search` tool, which caused Claude to:
1. Search for "papers"
2. Get text snippets mentioning papers
3. Search again for more details
4. Repeat 4-5 times trying to find the actual list
5. Give up and suggest visiting the website

**Solution**: Add dedicated tools that return complete, structured data directly.

## Available Tools

### 1. `list_papers` (NEW!)
**Best for**: "List all papers", "Show me your publications", "What papers have you published?"

Returns the complete list of academic papers in one call.

**Example usage in Claude Desktop**:
- "List all papers"
- "Show me Jan Henrik's publications"
- "What academic papers are there?"

**Output**: Full markdown content from papers.md (~1557 chars)

### 2. `get_cv` (NEW!)
**Best for**: "Show me your CV", "What's your work experience?", "Resume"

Returns the complete curriculum vitae.

**Example usage**:
- "Show me the CV"
- "What's Jan Henrik's work experience?"
- "Tell me about your background"

**Output**: Full CV content (~3000 chars)

### 3. `list_talks` (NEW!)
**Best for**: "List talks", "Show presentations", "What have you spoken about?"

Returns the complete list of public talks/presentations (in Norwegian: foredrag).

**Example usage**:
- "List all talks"
- "What presentations has Jan Henrik given?"
- "Show me the foredrag"

**Output**: Full talks content (~3400 chars)

### 4. `search`
**Best for**: Finding specific content across all documents

Use when you need to search for keywords that might appear anywhere in the site.

**Parameters**:
- `query` (string): Search term

**Example usage**:
- "Search for 'agile'"
- "Find mentions of 'OKR'"
- "Where is 'autonomous teams' discussed?"

**Output**: Concise list of matches with snippets (~500-1000 chars)

## Resource Access

In addition to tools, you can also read specific resources directly:

**Resource pattern**: `gundelsby://{path}`

**Examples**:
- `gundelsby://papers.md`
- `gundelsby://cv.md`
- `gundelsby://index.md`
- `gundelsby://_posts/2024-01-01-example.md`

## Performance Comparison

### Before (search only):

```
User: "List all papers"
→ Claude searches "papers"
→ Gets snippets mentioning papers
→ Searches "publications"
→ Gets more snippets
→ Searches specific terms found
→ Repeats 4-5 times
→ Result: "Visit the website"
Time: ~10-20 seconds, 4-5 tool calls
```

### After (with list_papers):

```
User: "List all papers"
→ Claude calls list_papers()
→ Gets complete list immediately
→ Result: Full formatted list of papers
Time: <1 second, 1 tool call
```

## Tool Selection Logic

Claude Desktop will automatically choose the best tool based on your query:

| Query | Tool Used | Why |
|-------|-----------|-----|
| "List all papers" | `list_papers()` | Direct match for papers |
| "Search for agile methodology" | `search("agile methodology")` | Keyword search needed |
| "Show me the CV" | `get_cv()` | Direct CV request |
| "What talks mention OKR?" | `search("OKR")` then context | Need to search, then filter |
| "List presentations" | `list_talks()` | Direct talks request |

## Testing the Tools

### From Command Line:
```bash
cd /Users/jhg/src/gundelsby.com/mcp
/Users/jhg/src/gundelsby.com/.venv/bin/python -c "
import asyncio
from gundelsby_mcp.server import list_papers

result = asyncio.run(list_papers())
print(result)
"
```

### In Claude Desktop:
After restarting Claude Desktop, try:
- "Use gundelsby to list all papers"
- "Show me Jan Henrik's CV using gundelsby"
- "List all talks from gundelsby"

## Next Steps

After updating the code:

1. **Quit Claude Desktop** (Cmd+Q)
2. **Restart Claude Desktop**
3. **Try the new tools**: "List all papers using gundelsby"

You should see instant results with just one tool call! 🚀
